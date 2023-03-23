from sqladmin import ModelAdmin
from starlette.requests import Request


class BaseModel(ModelAdmin):
    def is_accessible(self, request: Request) -> bool:
        """Only accessible by staff or admin"""
        user = request.user
        return user and user.is_authenticated and user.is_staff


class BaseModelAdminOnly(ModelAdmin):
    def is_accessible(self, request: Request) -> bool:
        """Only accessible by admin"""
        user = request.user
        return user and user.is_authenticated and user.is_admin
