from fastapi import Depends, File
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette_login.decorator import login_required

from sqlalchemy.ext.asyncio import AsyncSession

from apps.const import DIR_MEDIA
from apps.extensions.dependencies import get_db
from apps.extensions.template import templates
from apps.utils.notification import Notification
from .crud import UserCRUD
from .forms import UpdatePhotoForm, UpdateProfileForm

PROFILE_PICTURE_DIR = DIR_MEDIA / 'account'


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
        Notification(title='Updates saved').push(request)

    form_photo = await UpdatePhotoForm.from_formdata(request)
    context = {'request': request, 'form_photo': form_photo, 'form': form}
    return templates.TemplateResponse('account/profile_settings.html', context)


@login_required
async def update_photo_page(
    request: Request,
):
    db = get_db(request)
    form = await UpdatePhotoForm.from_formdata(request)
    user = request.user
    if await form.validate_on_submit():
        image_file, image_ext = await form.get_data()
        print(f'image_ext: {image_ext}')
        if image_ext == 'PNG':
            filename = f'u{str(user.id)}.png'
            filename_thumb = f'u{str(user.id)}-thumb.png'
        else:
            filename = f'u{str(user.id)}.jpg'
            filename_thumb = f'u{str(user.id)}-thumb.jpg'

        image_file.save(PROFILE_PICTURE_DIR / filename, image_ext)
        image_file.thumbnail((150, 150))
        image_file.save(PROFILE_PICTURE_DIR / filename_thumb, image_ext)

        await UserCRUD.update_photo(db, user.id, filename)
        Notification(title='Profile image updated').push(request)
    else:
        Notification(
            title='Profile image update failed', icon='error'
        ).push(request)
    return RedirectResponse(request.url_for('account:profile_settings'))
