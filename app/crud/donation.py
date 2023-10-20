from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.schemas.donation import DonationCreate


class CRUDDonation(
    CRUDBase[Donation, DonationCreate, BaseModel]
):
    """Класс CRUD-операций для модели Donation."""

    async def get_by_user(
        self,
        user: User,
        session: AsyncSession
    ) -> list[Donation]:
        """Получение списка пожертвований пользователя."""
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
