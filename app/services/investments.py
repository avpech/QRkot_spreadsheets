from datetime import datetime
from typing import TypeVar, Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.crud.charity_project import CRUDCharityProject, charity_project_crud
from app.crud.donation import CRUDDonation, donation_crud
from app.models import CharityProject, Donation

ModelType = TypeVar('ModelType', bound=Base)


def close_object(
    object: Union[CharityProject, Donation]
) -> None:
    """Закрытие проекта/пожертвования."""
    object.close_date = datetime.now()
    object.fully_invested = True


async def invest(
    allocated: ModelType,
    session: AsyncSession
) -> ModelType:
    """
    Распределение пожертвований по проектам.

    В аргумент allocated передается объект пожертования или проекта.
    При получении пожертвования распределяет средства по открытым проектам.
    При получении проекта вносит в него средства из открытых пожертвований.
    """
    crud: Union[CRUDCharityProject, CRUDDonation]
    if isinstance(allocated, CharityProject):
        crud = donation_crud
    elif isinstance(allocated, Donation):
        crud = charity_project_crud
    else:
        raise TypeError(
            'В параметр allocated передан объект недопустимого класса'
        )
    recipients = await crud.get_opened(session)
    if not recipients:
        return allocated
    for recipient in recipients:
        distribute = allocated.full_amount - (allocated.invested_amount or 0)
        recieve = recipient.full_amount - (recipient.invested_amount or 0)
        add = min(distribute, recieve)
        allocated.invested_amount = (allocated.invested_amount or 0) + add
        recipient.invested_amount = (recipient.invested_amount or 0) + add
        if distribute > recieve:
            close_object(recipient)
        elif distribute < recieve:
            close_object(allocated)
            break
        else:
            close_object(recipient)
            close_object(allocated)
            break
    return allocated
