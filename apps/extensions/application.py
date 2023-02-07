import logging

from starlette.applications import Starlette
from starlette.requests import Request
from sqlalchemy.ext.asyncio import async_scoped_session, AsyncSession

from apps.apps.account.crud import UserCRUD
from apps.core.configs import Base
from apps.core.error_handlers import add_error_handlers
from apps.core.middlewares import build_middlewares
from apps.core.routes import get_routes
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

    middleware = build_middlewares(config)

    # Session auth
    login_manager = create_login_manager(config.SECRET_KEY)
    middleware.append(get_middleware(login_manager))

    app = Starlette(
        debug=config.DEBUG,
        middleware=middleware,
        routes=get_routes(config)
    )

    app.state.login_manager = login_manager

    # Fastapi instance states
    app.state.config = config

    # Error handlers
    add_error_handlers(app)

    @app.middleware('http')
    async def set_extensions(request: Request, call_next):
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
                'errors/default.html',
                context={"request": request},
                status_code=500,
            )
        finally:
            assert response is not None
            secure_headers.framework.fastapi(response)
            return response

    @app.on_event('startup')
    async def startup():
        _db = db_session()
        # Create admin user
        await init_app(config, _db)
        login_manager.set_user_loader(user_loader)
        # setattr(login_manager, "session_maker", db_session)

    @app.on_event('shutdown')
    async def shutdown():
        if db_engine is not None:
            try:
                await db_engine.dispose()
            except:
                pass

    return app


async def init_app(configs: Base, db: AsyncSession):
    """create admin user"""
    if not await UserCRUD.get_by_username(db, 'admin'):
        await UserCRUD.create(
            db,
            username=configs.ADMIN_USERNAME,
            password=configs.ADMIN_PASSWORD,
            email=configs.ADMIN_EMAIL,
            first_name='Admin',
            last_name='',
            is_active=True, is_admin=True,
        )


async def user_loader(request: Request, user_id: int):
    db = request.state.db
    return await UserCRUD.get_by_id(db, user_id)
