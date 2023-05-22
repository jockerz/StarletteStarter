from PIL import Image
from starlette_babel import gettext_lazy as _
from starlette_wtf import StarletteForm
from wtforms import EmailField, FileField, PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo, Length


class UpdateEmailForm(StarletteForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = StringField(_('Password'), validators=[DataRequired()])


class UpdatePasswordForm(StarletteForm):
    old_password = PasswordField('Current Password', validators=[DataRequired()])
    password = PasswordField(
        _('New Password'),
        validators=[
            DataRequired(_('Please enter your password')),
            Length(min=8, message=_('Minimal 8 characters'))
        ]
    )
    confirm = PasswordField(
        _('Confirm Password'),
        validators=[EqualTo('password', message=_('Passwords don\'t match'))]
    )


class UpdateProfileForm(StarletteForm):
    name = StringField(_('Name'), validators=[DataRequired()])


class UpdatePhotoForm(StarletteForm):
    img = FileField(_('Image'), validators=[DataRequired()])

    async def get_data(self):
        content = self.img.data
        if content.headers.get('content-type') == 'image/png':
            image_type = 'PNG'
        else:
            image_type = 'JPEG'
        return Image.open(content.file._file).convert('RGB'), image_type
