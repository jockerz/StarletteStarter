from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette_login.utils import login_user, logout_user
from starlette_wtf import csrf_protect

from apps.core.logger import get_logger
from apps.extensions.dependencies import get_arq, get_config, get_db
from apps.extensions.template import templates
from apps.utils.notification import Notification
from apps.utils.url import validate_next_url
from apps.utils.string import mask_email
from apps.apps.account.crud import ActivationCRUD, UserCRUD, ResetCRUD
from .forms import (
    LoginForm,
    RegisterForm,
    ForgotPasswordForm,
    ResetPasswordForm
)
from .tasks import send_activation_message, send_reset_password

logger = get_logger()

login_success_notif = Notification(icon='success', title='Login Success')
login_failed_notif = Notification(
    text='Invalid username or password',
    icon='error', title='Authentication Failed'
)
login_inactive_notif = Notification(
    title='Account activation is required', category='alert'
)


async def home_page(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('main/home.html', context=context)


@csrf_protect
async def login_page(request: Request):
    db = get_db(request)
    form = await LoginForm.from_formdata(request)

    if await form.validate_on_submit():
        username = form.username.data
        if '@' in username:
            user = await UserCRUD.get_by_email(db, username)
        else:
            user = await UserCRUD.get_by_username(db, username)

        if user is not None and user.check_password(form.password.data):
            if user.is_active is False:
                login_inactive_notif.push(request)
            else:
                remember = form.remember_me.data
                await login_user(request, user, remember=remember)

                login_success_notif.push(request)
                next_url = validate_next_url(
                    request.query_params.get('next')
                ) or request.url_for('home')

                return RedirectResponse(next_url, status_code=302)
        else:
            login_failed_notif.push(request)
    context = {'request': request, 'form': form}
    return templates.TemplateResponse('main/login.html', context)


async def logout_page(request: Request) -> RedirectResponse:
    if request.user.is_authenticated:
        await logout_user(request)
    return RedirectResponse(request.url_for('home'), 303)


@csrf_protect
async def register_page(request: Request):
    arq = get_arq(request)
    config = get_config(request)
    db = get_db(request)
    form = await RegisterForm.from_formdata(request)

    if await form.validate_on_submit():
        if await UserCRUD.get_by_email(db, form.email.data):
            form.email.errors.append(
                'Email has been registered, please use another'
            )
        elif await UserCRUD.get_by_username(db, form.username.data):
            form.username.errors.append(
                'Username has been registered, please use another'
            )
        elif form.password.data != form.confirm.data:
            form.confirm.errors.append(
                'Password confirmation is not equal with the first password'
            )
        else:
            user = await UserCRUD.create(
                db, username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                name=form.name.data,
                commit=False
            )
            activation, secret = await ActivationCRUD.create(
                db, user, commit=False
            )

            db.add(user)
            db.add(activation)
            await db.commit()

            sent_to = activation.notif_type.name.lower()
            Notification(
                title='Registration complete',
                category='alert', icon='success',
                text=f'Activation URL is being sent to your {sent_to}'
            ).push(request)

            activation_url = request.url_for(
                'activation', code=activation.code, secret=secret
            )
            if config.TESTING is True:
                logger.debug(f"activation link: {activation_url}")
            else:
                await send_activation_message(
                    arq, recipient=activation.target,
                    activation_url=activation_url
                )
            return RedirectResponse('/login', 302)

    context = {'request': request, 'form': form}
    return templates.TemplateResponse('main/register.html', context)


async def activation_page(request: Request):
    db = get_db(request)

    code = request.path_params['code']
    secret = request.path_params['secret']
    if not code or not secret:
        raise HTTPException(404, 'Invalid activation code')

    success = False
    activation = await ActivationCRUD.get(db, code)
    if activation is None:
        raise HTTPException(404, 'Invalid activation code')
    elif activation.is_complete:
        raise HTTPException(404, 'Activation code has been used')
    elif activation.is_expired():
        raise HTTPException(404, 'Activation code has been expired')

    user = await UserCRUD.get_by_id(db, activation.user_id)
    if user is None:
        logger.error(f"Invalid user for activation code: {code}")
    elif user.is_active:
        Notification(title='User is already active').push(request)
    else:
        success, reason = ActivationCRUD.validate_secret(activation, secret)
        if success is False:
            Notification(
                title='Invalid activation code', category='alert'
            ).push(request)
        else:
            await ActivationCRUD.set_as_complete(db, activation, user)
    context = {'request': request, 'success': success}
    return templates.TemplateResponse('main/activation.html', context)


@csrf_protect
async def forgot_password_page(request: Request):
    # Redirect to next url or home page if user is already authenticated
    user = request.user
    if user and user.is_authenticated:
        next_url = validate_next_url(request.query_params.get('next', '/'))
        return RedirectResponse(request.url_for(next_url))

    arq = get_arq(request)
    db = get_db(request)
    form = await ForgotPasswordForm.from_formdata(request)
    context = {'request': request, 'form': form}

    if await form.validate_on_submit():
        email_username = form.email_username.data
        if '@' in email_username:
            user = await UserCRUD.get_by_email(db, email_username)
        else:
            user = await UserCRUD.get_by_username(db, email_username)

        if user is None:
            # Just send them a notification
            Notification(
                title=f'Password reset link has been sent to your email',
                category='alert'
            ).push(request)
        else:
            reset, secret = await ResetCRUD.create(db, user)

            reset_url = request.url_for(
                'reset_password', code=reset.code, secret=secret
            )
            if request.app.state.config.TESTING is True:
                logger.debug(f"reset link: {reset_url}")
            else:
                await send_reset_password(arq, reset.target, reset_url)
            Notification(
                title=f'Password reset link has been sent to '
                      f'{mask_email(reset.target)}',
                category='alert'
            ).push(request)

    return templates.TemplateResponse('main/forgot-password.html', context)


@csrf_protect
async def reset_password_page(request: Request):
    db = get_db(request)

    form = await ResetPasswordForm.from_formdata(request)

    code = request.path_params['code']
    secret = request.path_params['secret']
    if not code or not secret:
        raise HTTPException(404, 'Invalid password reset token')

    reset = await ResetCRUD.get(db, code)
    if reset is None:
        raise HTTPException(404, 'Invalid password reset code')

    user = await UserCRUD.get_by_id(db, reset.user_id)
    if user is None:
        logger.warning(f"Invalid user for activation code: {code}")

    success, reason = ResetCRUD.validate_secret(reset, secret)
    if success is True and await form.validate_on_submit():
        query = await UserCRUD.update_password(
            db, reset.user_id, form.password.data
        )
        await ResetCRUD.set_as_complete(db, reset, commit=False)
        await db.execute(query)
        db.add(reset)
        await db.commit()

        Notification(
            title='Password reset is complete', icon='success'
        ).push(request)

        next_url = validate_next_url(request.query_params.get('next', '/'))
        return RedirectResponse(next_url, 302)

    context = {'request': request, 'form': form, 'success': success}
    return templates.TemplateResponse('main/reset-password.html', context)
