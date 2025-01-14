from typing import AsyncGenerator
from uuid import UUID

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import registry

from marketgram.common.application.message_renderer import MessageRenderer
from marketgram.common.port.adapter.sqlalchemy_metadata import metadata
from marketgram.identity.access.domain.model.user import User
from marketgram.identity.access.port.adapter.argon2_password_hasher import Argon2PasswordHasher
from marketgram.identity.access.port.adapter.html_renderers import JwtTokenHtmlRenderer
from marketgram.identity.access.port.adapter.sqlalchemy_resources.identity_mapper import (
    identity_registry_mapper
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.identity_table import (
    role_table, 
    user_table, 
    web_session_table
)
from marketgram.identity.access.settings import (
    ActivateHtmlSettings, 
    ForgotPasswordHtmlSettings, 
    Settings, 
    identity_access_load_settings
)


mapper = registry()
identity_registry_mapper(mapper)


@pytest.fixture(scope='module')
def settings() -> Settings:
    return identity_access_load_settings()


@pytest_asyncio.fixture(loop_scope='session')
async def engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        'postgresql+psycopg://postgres:som@localhost:5433',
        echo=False,
    )
    async with engine.begin() as connection:
        await connection.run_sync(metadata.create_all)

    yield engine

    async with engine.begin() as connection:
        await connection.run_sync(metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope='function')
async def activate_msg_renderer(
    settings: Settings
) -> MessageRenderer[ActivateHtmlSettings, str]:
    return JwtTokenHtmlRenderer(
        settings.jinja_env, 
        settings.activate_html_settings
    )


@pytest.fixture(scope='function')
async def forgot_password_msg_renderer(
    settings: Settings
) -> MessageRenderer[ForgotPasswordHtmlSettings, str]:
    return JwtTokenHtmlRenderer(
        settings.jinja_env, 
        settings.forgot_pwd_html_settings
    )