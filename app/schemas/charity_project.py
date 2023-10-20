from datetime import datetime, timedelta
from typing import Optional

from pydantic import (BaseModel, Extra, Field, PositiveInt, root_validator,
                      validator)

from app.core.constants import MIN_ANY_STR_LENGTH, PROJECT_NAME_MAX_LENGTH


class CharityProjectBase(BaseModel):
    """Базовая схема для проектов."""

    class Config:
        min_anystr_length = MIN_ANY_STR_LENGTH
        anystr_strip_whitespace = True
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    """Схема для создания проектов."""
    name: str = Field(..., max_length=PROJECT_NAME_MAX_LENGTH)
    description: str
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    """Схема для изменения проектов."""
    name: Optional[str] = Field(None, max_length=PROJECT_NAME_MAX_LENGTH)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    @root_validator(pre=True)
    def field_cannot_be_null(
        cls,
        values: dict[str, Optional[str]]
    ) -> dict[str, Optional[str]]:
        """Валидация на недопустимость передачи полю значения null."""

        for field in ('name', 'description', 'full_amount'):
            if field in values and values[field] is None:
                raise ValueError(f'Значение поля {field} не может быть null.')
        return values


class CharityProjectDB(CharityProjectCreate):
    """Схема для получения данных о проектах."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectReadClosed(BaseModel):
    """Схема для отображения данных о закрытых проектах."""
    name: str
    gathering_time: str
    description: str

    @validator('gathering_time', pre=True)
    def convert_gathering_time_to_str(cls, value: timedelta):
        """Конвертация объекта timedelta в строку."""
        return str(value)

    class Config:
        extra = Extra.forbid
        schema_extra = {
            'example': {
                'name': 'string',
                'gathering_time': '1 day, 0:00:25.618390',
                'description': 'string'
            }
        }
