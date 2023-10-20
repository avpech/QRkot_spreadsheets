from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject


class ErrorMessages:
    NAME_DUPLICATE = 'Проект с таким именем уже существует!'
    NOT_FOUND = 'Проект не найден'
    PROJECT_CLOSED = 'Закрытый проект нельзя редактировать!'
    PROJECT_INVESTED = 'В проект были внесены средства, не подлежит удалению!'
    INCORRECT_FULL_AMOUNT = (
        'Нельзя установить требуемую сумму меньше уже вложенной.'
    )


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """Проверка на отсутствие проекта с переданным именем в базе данных."""
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name=project_name, session=session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorMessages.NAME_DUPLICATE,
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Возвращает проект с переданным id, если он есть в базе данных."""
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ErrorMessages.NOT_FOUND
        )
    return project


async def check_full_amount_ge_invested_amount(
    full_amount: int,
    invested_amount: int
) -> None:
    """Проверка на то, что требуемая сумма не меньше уже вложенной."""
    if full_amount < invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=ErrorMessages.INCORRECT_FULL_AMOUNT
        )


async def check_project_is_opened(project: CharityProject) -> None:
    """Проверка на то, что проект открыт."""
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorMessages.PROJECT_CLOSED
        )


async def check_project_is_not_invested(project: CharityProject) -> None:
    """Проверка на то, что в проект не были инвестированы средства."""
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorMessages.PROJECT_INVESTED
        )
