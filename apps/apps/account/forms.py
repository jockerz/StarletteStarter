from PIL import Image
from starlette_wtf import StarletteForm
from wtforms import BooleanField, FileField, StringField
from wtforms.validators import DataRequired


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
