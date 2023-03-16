from starlette.responses import JSONResponse
from starlette.routing import Route

from apps.apps.main.forms import (
    LoginForm,
    RegisterForm,
    ForgotPasswordForm,
    ResetPasswordForm
)

URL = '/test_form'


async def login_form_page(request):
    form = await LoginForm.from_formdata(request)
    if await form.validate():
        return JSONResponse(form.data)
    else:
        return JSONResponse(form.data, status_code=400)


async def register_form_page(request):
    form = await RegisterForm.from_formdata(request)
    if await form.validate():
        return JSONResponse(form.data)
    else:
        return JSONResponse(form.data, status_code=400)


async def forgot_pass_page(request):
    form = await ForgotPasswordForm.from_formdata(request)
    if await form.validate():
        return JSONResponse(form.data)
    else:
        return JSONResponse(form.data, status_code=400)


async def reset_pass_page(request):
    form = await ResetPasswordForm.from_formdata(request)
    if await form.validate():
        return JSONResponse(form.data)
    else:
        return JSONResponse(form.data, status_code=400)


class TestLoginForm:
    async def test_success(self, application, http):
        application.routes.append(
            Route(URL, login_form_page, methods=['POST'])
        )

        form_data = {'username': 'username', 'password': 'password'}
        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 200

        form_data = {'username': 'email@email.com', 'password': 'password'}
        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 200

        form_data['remember_me'] = True

        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 200

    async def test_fails(self, application, http):
        application.routes.append(
            Route(URL, login_form_page, methods=['POST'])
        )
        resp = await http.post(URL, form={'username': 'username'})
        assert resp.status_code == 400

        resp = await http.post(URL, form={'password': 'password'})
        assert resp.status_code == 400


class TestRegisterForm:
    async def test_success(self, application, http):
        application.routes.append(
            Route(URL, register_form_page, methods=['POST'])
        )

        form_data = {
            'username': 'username',
            'email': 'email@email.com',
            'password': 'password',
            'confirm': 'password',
            'name': 'Full Name',
            'agree_terms': True
        }
        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 200

    async def test_fail_invalid_email(self, application, http):
        application.routes.append(
            Route(URL, register_form_page, methods=['POST'])
        )

        form_data = {
            'username': 'username',
            'email': 'invalid_email',
            'password': 'password',
            'confirm': 'password',
            'name': 'Full Name',
            'agree_terms': True
        }
        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 400

    async def test_fail_invalid_username(self, application, http):
        application.routes.append(
            Route(URL, register_form_page, methods=['POST'])
        )

        form_data = {
            'username': 'inv',
            'email': 'email@email.com',
            'password': 'password',
            'confirm': 'password',
            'name': 'Full Name',
            'agree_terms': True
        }
        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 400

    async def test_fail_invalid_password(self, application, http):
        application.routes.append(
            Route(URL, register_form_page, methods=['POST'])
        )

        form_data = {
            'username': 'username',
            'email': 'email@email.com',
            'password': 'invalid',
            'confirm': 'invalid',
            'name': 'Full Name',
            'agree_terms': True
        }
        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 400

    async def test_fail_invalid_confirm(self, application, http):
        application.routes.append(
            Route(URL, register_form_page, methods=['POST'])
        )

        form_data = {
            'username': 'username',
            'email': 'email@email.com',
            'password': 'password',
            'confirm': 'false_confirm',
            'name': 'Full Name',
            'agree_terms': True
        }
        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 400

    async def test_fail_invalid_name(self, application, http):
        application.routes.append(
            Route(URL, register_form_page, methods=['POST'])
        )

        form_data = {
            'username': 'username',
            'email': 'email@email.com',
            'password': 'password',
            'confirm': 'false_confirm',
            'agree_terms': True
        }
        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 400

    async def test_fail_invalid_terms_agreements(self, application, http):
        application.routes.append(
            Route(URL, register_form_page, methods=['POST'])
        )

        form_data = {
            'username': 'username',
            'email': 'email@email.com',
            'password': 'password',
            'confirm': 'password',
            'agree_terms': False
        }
        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 400


class TestForgotPasswordForm:
    def prepare(self, application):
        application.routes.append(
            Route(URL, forgot_pass_page, methods=['POST'])
        )

    async def test_success(self, application, http):
        self.prepare(application)

        form_data = {'email_username': 'username'}
        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 200

        form_data = {'email_username': 'email@mai.com'}
        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 200

    async def test_fails(self, application, http):
        self.prepare(application)
        resp = await http.post(URL, form={})
        assert resp.status_code == 400


class TestResetPasswordForm:
    def prepare(self, application):
        application.routes.append(
            Route(URL, reset_pass_page, methods=['POST'])
        )

    async def test_success(self, application, http):
        self.prepare(application)

        form_data = {'password': 'password', 'confirm': 'password'}
        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 200

    async def test_fail_invalid_password(self, application, http):
        self.prepare(application)

        form_data = {'password': 'short', 'confirm': 'short'}
        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 400

    async def test_fail_invalid_confirm(self, application, http):
        self.prepare(application)

        form_data = {'password': 'password', 'confirm': 'invalid_pass'}
        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 400
