from starlette_wtf import StarletteForm
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import (
    AnyOf, DataRequired, Email, EqualTo, Length
)