import pytest_asyncio

from apps.apps.oauth2.crud import OAuth2AccountCRUD
from apps.apps.oauth2.models import ProviderEnum


@pytest_asyncio.fixture
async def social_account(db, user):
    provider = ProviderEnum.github
    return await OAuth2AccountCRUD.get_by_user_id(db, user.id, provider) \
        or await OAuth2AccountCRUD.create(
            db, provider, user, 'UID', user.username
        )
