from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from apps.apps.account.forms import (
    UpdateEmailForm,
    UpdatePasswordForm,
    UpdatePhotoForm,
    UpdateProfileForm
)


URL = '/test_form'


class TestUpdateEmailForm:
    async def test_success(self, application: Starlette, http):
        form_data = {'email': 'email@mai.com', 'password': 'password'}

        async def index(request):
            form = await UpdateEmailForm.from_formdata(request)
            assert form.email.data == form_data['email']
            assert form.password.data == form_data['password']
            if await form.validate():
                return JSONResponse(form.data)
            else:
                return JSONResponse(form.data, status_code=400)

        application.routes.append(Route(URL, index, methods=['POST']))
        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 200

    async def test_fails(self, application: Starlette, http):
        async def index(request):
            form = await UpdateEmailForm.from_formdata(request)
            if await form.validate():
                return JSONResponse(form.data)
            else:
                return JSONResponse(form.data, status_code=400)

        application.routes.append(Route(URL, index, methods=['POST']))
        resp = await http.post(URL, form={'email': 'email@mai.com'})
        assert resp.status_code == 400

        resp = await http.post(URL, form={'password': 'password'})
        assert resp.status_code == 400


class TestUpdatePasswordForm:
    async def test_success(self, application: Starlette, http):
        form_data = {
            'old_password': 'old_password',
            'password': 'password',
            'confirm': 'password',
        }

        async def index(request):
            form = await UpdatePasswordForm.from_formdata(request)
            if await form.validate():
                return JSONResponse(form.data)
            else:
                return JSONResponse(form.errors, status_code=400)

        application.routes.append(Route(URL, index, methods=['POST']))
        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 200, resp.json()

    async def test_fail_false_confirm(self, application: Starlette, http):
        form_data = {
            'old_password': 'old_password',
            'password': 'password',
            'confirm': 'false_confirm',
        }

        async def index(request):
            form = await UpdatePasswordForm.from_formdata(request)
            if await form.validate():
                return JSONResponse(form.data)
            else:
                return JSONResponse(form.data, status_code=400)

        application.routes.append(Route(URL, index, methods=['POST']))
        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 400

    async def test_fail_empty_old_password(self, application: Starlette, http):
        form_data = {'password': 'password', 'confirm': 'password'}

        async def index(request):
            form = await UpdatePasswordForm.from_formdata(request)
            if await form.validate():
                return JSONResponse(form.data)
            else:
                return JSONResponse(form.data, status_code=400)

        application.routes.append(Route(URL, index, methods=['POST']))
        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 400

    async def test_fail_empty_new_password(self, application: Starlette, http):
        form_data = {'old_password': 'old_password', 'confirm': 'password'}

        async def index(request):
            form = await UpdatePasswordForm.from_formdata(request)
            if await form.validate():
                return JSONResponse(form.data)
            else:
                return JSONResponse(form.data, status_code=400)

        application.routes.append(Route(URL, index, methods=['POST']))
        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 400

    async def test_fail_less_than_8(self, application: Starlette, http):
        form_data = {
            'old_password': 'old_password',
            'password': 'less8',
            'confirm': 'less8',
        }

        async def index(request):
            form = await UpdatePasswordForm.from_formdata(request)
            if await form.validate():
                return JSONResponse(form.data)
            else:
                return JSONResponse(form.data, status_code=400)

        application.routes.append(Route(URL, index, methods=['POST']))
        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 400


class TestUpdatePhotoForm:
    async def test_success(self, application: Starlette, http):
        form_data = {'img': b'data'}

        async def index(request):
            form = await UpdatePhotoForm.from_formdata(request)
            if await form.validate():
                return JSONResponse(form.data)
            else:
                return JSONResponse(form.data, status_code=400)

        application.routes.append(Route(URL, index, methods=['POST']))
        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 200, resp.json()

    async def test_fails(self, application: Starlette, http):
        async def index(request):
            form = await UpdatePhotoForm.from_formdata(request)
            if await form.validate():
                return JSONResponse(form.data)
            else:
                return JSONResponse(form.data, status_code=400)

        application.routes.append(Route(URL, index, methods=['POST']))
        resp = await http.post(URL, form={})
        assert resp.status_code == 400


class TestUpdateProfileForm:
    async def test_success(self, application: Starlette, http):
        form_data = {'name': 'Name'}

        async def index(request):
            form = await UpdateProfileForm.from_formdata(request)
            if await form.validate():
                return JSONResponse(form.data)
            else:
                return JSONResponse(form.data, status_code=400)

        application.routes.append(Route(URL, index, methods=['POST']))
        resp = await http.post(URL, form=form_data)
        assert resp.status_code == 200, resp.json()

    async def test_fails(self, application: Starlette, http):
        async def index(request):
            form = await UpdateProfileForm.from_formdata(request)
            if await form.validate():
                return JSONResponse(form.data)
            else:
                return JSONResponse(form.data, status_code=400)

        application.routes.append(Route(URL, index, methods=['POST']))
        resp = await http.post(URL, form={})
        assert resp.status_code == 400
