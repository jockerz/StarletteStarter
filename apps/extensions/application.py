import contextlib
import logging

from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from sqlalchemy.ext.asyncio import async_scoped_session, AsyncSession

from apps.apps.account.crud import UserCRUD
from apps.core.admin import register_models
from apps.core.configs import Base
from apps.core.error_handlers import get_error_handlers
from apps.core.middlewares import build_middlewares
from apps.core.routes import get_routes
from apps.extensions.oauth2 import create_oauth2
from .admin import create_admin
from .arq import create_connection
from .db import create_db_engine, create_db_session, create_scope_session
from .login_manager import create_login_manager, get_middleware
from .secure import secure_headers
from .template import templates

logger = logging.getLogger('uvicorn.error')


def create_application(
    config: Base,
    db_session: async_scoped_session = None,
) -> Starlette:
    """
    Create the FastAPI instance with the desired configuration

    :param config: Configuration
    :param db_session: only to be used in test fixture
    :return: a ready to use FastAPI instance
    """
    if db_session is None:
        # Create DB engine and scoped session
        db_engine = create_db_engine(config.DATABASE_URL)
        db_session = create_scope_session(create_db_session(db_engine))
    else:
        # on `pytest` `application` fixture, we should include
        # db_session argument
        db_engine = None

    # Session auth
    login_manager = create_login_manager(config.SECRET_KEY)

    # middlewares
    middleware = build_middlewares(config)
    middleware.append(get_middleware(login_manager))

    # @app.on_event('startup')
    async def startup():
        _db = db_session()
        # Create admin user
        await init_app(config, _db)
        login_manager.set_user_loader(user_loader)

        app.state.arq = await create_connection(config)

    # @app.on_event('shutdown')
    async def shutdown():
        if db_engine is not None:
            try:
                await db_engine.dispose()
            except:
                pass

    @contextlib.asynccontextmanager
    async def lifespan(app):
        """docs: https://www.starlette.io/lifespan/"""
        await startup()
        yield
        await shutdown()

    app = Starlette(
        debug=config.DEBUG, middleware=middleware,
        routes=get_routes(config), lifespan=lifespan
    )

    # Application states
    app.state.config = config
    app.state.login_manager = login_manager
    app.state.oauth2 = create_oauth2(config)

    # Skip testing
    if config.TESTING is False:
        # Admin
        admin = create_admin(app, db_engine, middleware, config.DEBUG)
        register_models(admin)

    # Error handlers
    app.exception_handlers.update(get_error_handlers())

    class CustomMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            response = None
            try:
                # DB Session
                request.state.db = db_session()

                # Process the request
                response = await call_next(request)

                # close DB Session
                await request.state.db.close()

            except Exception as exc:
                logger.exception(exc)
                response = templates.TemplateResponse(
                    'errors/default.html', context={"request": request},
                    status_code=500,
                )
            finally:
                assert response is not None
                secure_headers.framework.fastapi(response)
                return response

    # Request state setup middleware
    app.add_middleware(CustomMiddleware)

    return app


async def init_app(config: Base, db: AsyncSession):
    """create admin user"""
    # validate email, username and password
    if not config.ADMIN_EMAIL:
        raise ValueError('Invalid ADMIN_EMAIL value')
    elif not config.ADMIN_USERNAME:
        raise ValueError('Invalid ADMIN_USERNAME value')
    elif not config.ADMIN_PASSWORD:
        raise ValueError('Invalid ADMIN_PASSWORD value')
    elif len(config.ADMIN_PASSWORD) < 8:
        raise ValueError('Invalid ADMIN_PASSWORD length. min: 10')

    if not await UserCRUD.get_by_username(db, config.ADMIN_USERNAME):
        await UserCRUD.create(
            db,
            username=config.ADMIN_USERNAME,
            password=config.ADMIN_PASSWORD,
            email=config.ADMIN_EMAIL,
            name=config.ADMIN_NAME,
            is_active=True, is_admin=True,
        )
        logger.info('Admin created')


async def user_loader(request: Request, user_id: int):
    db = request.state.db
    return await UserCRUD.get_by_id(db, user_id)
