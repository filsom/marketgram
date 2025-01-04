from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID, uuid4

from marketgram.identity.access.domain.model.role_repository import (
    RoleRepository
)
from marketgram.identity.access.domain.model.web_session_service import (
    WebSessionService
)


@dataclass
class GetUserFields:
    session_id: UUID


class GetUser:
    def __init__(
        self,
        web_session_service: WebSessionService,
        role_repository: RoleRepository,
    ) -> None:
        self._web_session_service = web_session_service
        self._role_repository = role_repository

    async def execute(self, fields: GetUserFields) -> dict[str, str]:
        return await self._web_session_service \
            .extend(
                fields.session_id,
                uuid4(),
                datetime.now(UTC)
            )