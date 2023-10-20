from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_full_amount_ge_invested_amount,
                                check_name_duplicate, check_project_exists,
                                check_project_is_not_invested,
                                check_project_is_opened)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investments import invest

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),)
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Создать благотворительный проект. Только для суперпользователей.

    - **name**: Название проекта.
    - **description**: Описание проекта.
    - **full_amount**: Требуемая сумма.
    """
    await check_name_duplicate(
        project_name=project.name, session=session
    )
    new_project = await charity_project_crud.create(
        obj_in=project, session=session, commit=False
    )
    new_project = await invest(allocated=new_project, session=session)
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model_exclude_none=True,
    response_model=list[CharityProjectDB]
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Получить список всех проектов."""
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=(Depends(current_superuser),)
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Изменить благотворительный проект. Только для суперпользователей.

    Нельзя измененить закрытый проект.
    - **name**: Название проекта.
    - **description**: Описание проекта.
    - **full_amount**: Требуемая сумма.
    """
    project = await check_project_exists(
        project_id=project_id, session=session
    )
    await check_project_is_opened(project)
    if obj_in.name is not None:
        await check_name_duplicate(project_name=obj_in.name, session=session)
    if obj_in.full_amount is not None:
        await check_full_amount_ge_invested_amount(
            full_amount=obj_in.full_amount,
            invested_amount=project.invested_amount
        )
    return await charity_project_crud.update(
        db_obj=project, obj_in=obj_in, session=session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=(Depends(current_superuser),)
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Удалить проект. Только для суперпользователей.

    Нельзя удалить проект, в который уже были инвестированы средства,
    его можно только закрыть.
    """
    project = await check_project_exists(
        project_id=project_id, session=session
    )
    await check_project_is_not_invested(project)
    return await charity_project_crud.remove(
        db_obj=project, session=session
    )
