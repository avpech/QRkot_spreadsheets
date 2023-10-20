from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.custom_types import ProjectClosedDict
from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectUpdate)


class CRUDCharityProject(
    CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate]
):
    """Класс CRUD-операций для модели CharityProject."""

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        """Получение id проекта по его названию."""
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ) -> list[ProjectClosedDict]:
        """Получение списка с данными о закрытых проектах."""
        projects = await session.execute(
            select(CharityProject).where(CharityProject.fully_invested)
        )
        projects = projects.scalars().all()
        return sorted(
            [
                {
                    'name': project.name,
                    'gathering_time': project.close_date - project.create_date,
                    'description': project.description
                } for project in projects
            ],
            key=lambda elem: elem['gathering_time']
        )


charity_project_crud = CRUDCharityProject(CharityProject)
