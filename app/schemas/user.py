from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема для получения данных о пользователе."""
    pass


class UserCreate(schemas.BaseUserCreate):
    """Схема для создания пользователя."""
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Схема для изменения пользователя."""
    pass
