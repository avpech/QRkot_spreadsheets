from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base
from app.models.mixins import CharityMixin


class Donation(CharityMixin, Base):
    """Модель для пожертвований."""
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user'),
        nullable=False
    )
    comment = Column(Text)
