from dataclasses import dataclass

from marketgram.common.application.email_sender import EmailSender
from marketgram.common.application.handler import Command
from marketgram.common.application.message_renderer import MessageRenderer
from marketgram.common.application.jwt_manager import TokenManager
from marketgram.identity.access.domain.model.user_repository import (
    UserRepository
)
from marketgram.identity.access.settings import ForgotPasswordHtmlSettings


@dataclass
class ForgotPasswordCommand(Command):
    email: str


class ForgotPasswordHandler:
    def __init__(
        self,
        user_repository: UserRepository,
        jwt_manager: TokenManager,
        message_renderer: MessageRenderer[
            ForgotPasswordHtmlSettings, str
        ],
        email_sender: EmailSender
    ) -> None:
        self._user_repository = user_repository
        self._jwt_manager = jwt_manager
        self._message_renderer = message_renderer
        self._email_sender = email_sender
    
    async def handle(self, command: ForgotPasswordCommand) -> None:
        user = await self._user_repository.with_email(command.email)
        
        if user is None or not user.is_active:
            return 
        
        jwt_token = self._jwt_manager.encode({
            'sub': user.to_string_id(),
            'aud': 'user:password'
        })
        message = self._message_renderer.render(user.email, jwt_token)

        return await self._email_sender.send_message(message)