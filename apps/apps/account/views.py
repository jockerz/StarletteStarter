from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette_babel import gettext_lazy as _
from starlette_login.decorator import login_required

from apps.const import DIR_MEDIA
from apps.core.logger import get_logger
from apps.extensions.dependencies import get_config, get_db, get_saq
from apps.extensions.template import templates
from apps.utils.notification import Notification
from .crud import EmailUpdateCRUD, UserCRUD
from .forms import (
    UpdateEmailForm,
    UpdatePasswordForm,
    UpdatePhotoForm,
    UpdateProfileForm
)
from .models import User
from .tasks import send_validate_email

PROFILE_PICTURE_DIR = DIR_MEDIA / 'account'

logger = get_logger()


@login_required
async def profile_page(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('account/profile.html', context)


@login_required
async def profile_settings_page(request: Request):
    db = get_db(request)
    user = request.user
    form = await UpdateProfileForm.from_formdata(request)
    if await form.validate_on_submit():
        await UserCRUD.update_data(db, user.id, form.name.data)
        Notification(title=_('Updates saved')).push(request)

    form_photo = await UpdatePhotoForm.from_formdata(request)
    context = {'request': request, 'form_photo': form_photo, 'form': form}
    return templates.TemplateResponse('account/profile_settings.html', context)


@login_required
async def update_password_page(request: Request):
    db = get_db(request)
    user = request.user
    form = await UpdatePasswordForm.from_formdata(request)
    if await form.validate_on_submit():
        if not user.check_password(form.old_password.data):
            form.old_password.errors.append(_('Invalid password'))
        else:
            await UserCRUD.update_password(db, user.id, form.password.data)
            Notification(title=_('Password has been updated')).push(request)

    context = {'request': request, 'form': form}
    return templates.TemplateResponse('account/password_update.html', context)


@login_required
async def update_photo_page(request: Request):
    db = get_db(request)
    form = await UpdatePhotoForm.from_formdata(request)
    user = request.user
    if await form.validate_on_submit():
        image_file, image_ext = await form.get_data()
        image_ext = image_ext.lower()
        filename = f'u{str(user.id)}.{image_ext}'
        filename_thumb = f'u{str(user.id)}-thumb.{image_ext}'

        image_file.save(PROFILE_PICTURE_DIR / filename, image_ext)
        image_file.thumbnail((150, 150))
        image_file.save(PROFILE_PICTURE_DIR / filename_thumb, image_ext)

        await UserCRUD.update_photo(db, user.id, filename)
        Notification(title=_('Profile image updated')).push(request)
    else:
        Notification(
            title=_('Profile image update failed'),
            icon='error'
        ).push(request)
    return RedirectResponse(
        request.url_for('account:profile_settings'),
        status_code=302
    )


@login_required
async def email_settings_page(request: Request):
    config = get_config(request)
    db = get_db(request)
    form = await UpdateEmailForm.from_formdata(request)
    user: User = request.user
    if await form.validate_on_submit():
        new_email = form.email.data.strip().lower()

        if not user.check_password(form.password.data):
            form.password.errors.append(_('Invalid password'))
        elif user.email == new_email:
            form.email.errors.append(_('Email not changed'))
        else:
            saq = get_saq(request)

            token, secret = await EmailUpdateCRUD.create(db, user, new_email)

            notif_text = _('Email update URL is being sent to {new_email}')
            Notification(
                title=_('Visit Email update URL to save email changes'),
                category='alert',
                icon='success',
                text=notif_text.format(new_email=new_email)
            ).push(request)

            email_update_url = request.url_for(
                'account:email_update', code=token.code, secret=secret
            )
            if config.TESTING is True:
                logger.debug(f"Email update link: {email_update_url}")
            else:
                await send_validate_email(saq, new_email, email_update_url)
    context = {'request': request, 'form': form}
    return templates.TemplateResponse('account/email_settings.html', context)


@login_required
async def email_update_page(request: Request):
    db = get_db(request)
    user: User = request.user

    code = request.path_params['code']
    secret = request.path_params['secret']
    if not code or not secret:
        raise HTTPException(404, _('Invalid activation code'))

    token = await EmailUpdateCRUD.get(db, code)
    if token is None:
        raise HTTPException(404, _('Invalid Email Update URL'))
    elif token.is_complete:
        raise HTTPException(400, _('Email Update link has been used'))
    elif token.is_expired():
        raise HTTPException(400, _('Email Update link has been expired'))

    success, reason = EmailUpdateCRUD.validate_secret(token, secret)
    if success is False:
        Notification(
            title=_('Invalid activation code'),
            category='alert'
        ).push(request)
    else:
        await EmailUpdateCRUD.set_as_complete(db, token, user)

    context = {'request': request, 'success': success}
    return templates.TemplateResponse('account/email_update.html', context)
