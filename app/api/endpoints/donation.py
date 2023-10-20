from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationDBFull
from app.services.investments import invest

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Сделать пожертвование.

    - **full_amount**: Сумма пожертвования.
    - **comment**: Комментарий к пожертвованию (опционально).
    """
    new_donation = await donation_crud.create(
        obj_in=donation, session=session, user=user, commit=False
    )
    new_donation = await invest(allocated=new_donation, session=session)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDBFull],
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),)
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Получить список всех пожертвований. Только для суперпользователей."""
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationDB]
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Получить список пожертвований текущего пользователя."""
    return await donation_crud.get_by_user(user=user, session=session)
