from sqlalchemy.orm import registry

from marketgram.identity.access.domain.model.user import User
from marketgram.identity.access.port.adapter.sqlalchemy_resources.mapping.table.user_table import (
    user_table
)


def user_registry_mapper(mapper: registry):
    mapper.map_imperatively(
        User,
        user_table,
        properties={
            '_user_id': user_table.c.user_id,
            '_email': user_table.c.email,
            '_password': user_table.c.password,
            '_is_active': user_table.c.is_active,
        },
        column_prefix="_",
        version_id_col=user_table.c.version_id,
    )