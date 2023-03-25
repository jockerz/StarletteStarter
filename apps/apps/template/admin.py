from apps.core.base.admin import BaseModel

from .models import NewModel


class NewModelAdmin(BaseModel, model=NewModel):
    column_list = [
        NewModel.id, NewModel.name
    ]
