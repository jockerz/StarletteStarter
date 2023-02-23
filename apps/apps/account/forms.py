from PIL import Image
from starlette_wtf import StarletteForm
from wtforms import EmailField, FileField, PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo, Length


class UpdateEmailForm(StarletteForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])


class UpdatePasswordForm(StarletteForm):
    old_password = PasswordField('Current Password', validators=[DataRequired()])
    password = PasswordField(
        'New Password',
        validators=[
            DataRequired('Please enter your password'),
            Length(min=8, message='Minimal 8 characters')
        ]
    )
    confirm = PasswordField(
        'Confirm Password',
        validators=[EqualTo('password', message='Passwords don\'t match')]
    )


class UpdateProfileForm(StarletteForm):
    name = StringField('Name', validators=[DataRequired()])


class UpdatePhotoForm(StarletteForm):
    img = FileField('Image', validators=[DataRequired()])

    async def get_data(self):
        content = self.img.data
        if content.headers.get('content-type') == 'image/png':
            image_type = 'PNG'
        else:
            image_type = 'JPEG'
        return Image.open(content.file._file).convert('RGB'), image_type
