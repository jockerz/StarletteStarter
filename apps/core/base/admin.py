import logging
from typing import Any, Optional

from sqladmin import ModelView
from starlette.requests import Request


logger = logging.getLogger('uvicorn.error')


def log_message(data: Optional[dict], model: Any, action: str):
    if data is None:
        data = ''
    msg = f'[ADMIN] action={action} data="{data}" model={model}'
    logger.warning(msg)


class BaseModel(ModelView):
    can_delete = False

    def is_accessible(self, request: Request) -> bool:
        """Only accessible by staff or admin"""
        user = request.user
        return user and user.is_authenticated and user.is_staff

    async def after_model_change(
        self, data: dict, model: Any, is_created: bool
    ) -> None:
        action = 'create' if is_created else 'update'
        log_message(data, model, action=action)

    async def after_model_delete(self, model: Any) -> None:
        log_message(None, model, action='delete')


class BaseModelAdminOnly(BaseModel):
    def is_accessible(self, request: Request) -> bool:
        """Only accessible by admin"""
        user = request.user
        return user and user.is_authenticated and user.is_admin
