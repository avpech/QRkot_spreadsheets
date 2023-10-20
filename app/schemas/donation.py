from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationCreate(BaseModel):
    """Схема для создания пожертвований."""
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        anystr_strip_whitespace = True
        extra = Extra.forbid


class DonationDB(DonationCreate):
    """Краткая схема для получения данных о пожертвованиях."""
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBFull(DonationDB):
    """Расширенная схема для получения данных о пожертвованиях."""
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
