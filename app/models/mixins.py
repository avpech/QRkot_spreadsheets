from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer


class CharityMixin:
    """Миксин с общими полями для моделей пожертвований и проектов."""
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now)
    close_date = Column(DateTime)
    __table_args__ = (
        CheckConstraint(
            'full_amount >= invested_amount',
            name='full_amount_gt_invested_amount'
        ),
        CheckConstraint(
            'full_amount > 0',
            name='full_amount_positive'
        ),
        CheckConstraint(
            'invested_amount >= 0',
            name='invested_amount_not_negative'
        ),
    )
