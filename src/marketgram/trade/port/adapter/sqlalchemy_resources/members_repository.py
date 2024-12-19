from uuid import UUID

from marketgram.trade.domain.model.p2p_2.seller import Seller
from marketgram.trade.domain.model.p2p_2.user import User

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select, func
from sqlalchemy.orm import with_expression

from marketgram.trade.domain.model.rule.agreement.entry_status import EntryStatus
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.entries_table import (
    entries_table
)


class SQLAlchemyMembersRepository:
    def __init__(
        self,
        async_session: AsyncSession
    ) -> None:
        self._async_session = async_session

    def add(self, seller: Seller) -> None:
        self._async_session.add(seller)
    
    async def seller_with_id(self, user_id: UUID) -> Seller | None:
        stmt = select(Seller).where(Seller._user_id == user_id)
        result = await self._async_session.execute(stmt)
        
        return result.scalar_one_or_none()

    async def seller_with_balance_and_id(self, user_id: UUID) -> Seller | None:
        stmt = (
            select(Seller)
            .where(Seller._user_id == user_id)
            .options(with_expression(
                Seller._balance, 
                self._sum_query(user_id)
            ))
            .with_for_update()
        )
        result = await self._async_session.execute(stmt)
        
        return result.scalar()
    
    async def user_with_id(self, user_id: UUID) -> User | None:
        stmt = select(User).where(User._user_id == user_id)
        result = await self._async_session.execute(stmt)
        
        return result.scalar_one_or_none()
    
    async def user_with_balance_and_id(self, user_id: UUID) -> User | None:
        stmt = (
            select(User)
            .where(User._user_id == user_id)
            .options(with_expression(User._balance, self._sum_query(user_id)))
            .with_for_update()
        )
        result = await self._async_session.execute(stmt)
        
        return result.scalar()
    
    def _sum_query(self, user_id: UUID):
        return (
            select(func.sum(entries_table.c.amount))
            .where(and_(
                entries_table.c.user_id == user_id,
                # entries_table.c.entry_status == EntryStatus.ACCEPTED
            ))
            .scalar_subquery()
        )