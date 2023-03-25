from starlette_wtf import StarletteForm
from wtforms import StringField
from wtforms.validators import DataRequired


class Form(StarletteForm):
    data = StringField('Data', validators=[DataRequired()])
