from sqlalchemy import Column, String, Text

from app.core.constants import PROJECT_NAME_MAX_LENGTH
from app.core.db import Base
from app.models.mixins import CharityMixin


class CharityProject(CharityMixin, Base):
    """Модель для благотворительных проектов."""
    name = Column(
        String(PROJECT_NAME_MAX_LENGTH),
        unique=True,
        nullable=False
    )
    description = Column(Text, nullable=False)
