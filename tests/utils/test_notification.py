from starlette.requests import Request
from starlette.routing import Route

from apps.utils.notification import FLASH_SESSION_NAME, Notification


notification = Notification(
    title='title',
    icon='info',
    text='text',
    footer='footer',
    category='alert'
)


class TestNotification:
    def test_session_name(self):
        assert FLASH_SESSION_NAME == '_flash'

    async def test_notification(self, application, http):
        async def test_notification(request: Request):
            notification.push(request)
            assert FLASH_SESSION_NAME in request.scope['session']
            return {'success': FLASH_SESSION_NAME in request.scope['session']}

        application.router.routes.append(
            Route('/test_notification', test_notification)
        )

        await http.get('/test_notification')
