from starlette_wtf import StarletteForm
from wtforms import SelectField

from .models import ProviderEnum


class LinkProviderForm(StarletteForm):
    provider = SelectField('Provider', choices=[
        ProviderEnum.github.value
    ])

    def to_enum(self):
        try:
            return ProviderEnum(self.provider.data)
        except ValueError:
            pass
