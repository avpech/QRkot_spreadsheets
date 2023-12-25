from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.custom_types import ProjectClosedDict

FORMAT = '%Y/%m/%d %H:%M:%S'
DRIVE_SERVICE = 'drive'
DRIVE_VERSION = 'v3'
SHEET_SERVICE = 'sheets'
SHEET_VERSION = 'v4'
SHEETS = [
    {'properties': {'sheetType': 'GRID',
                    'sheetId': 0,
                    'title': 'Лист1',
                    'gridProperties': {'rowCount': 100,
                                       'columnCount': 11}}}
]


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создание гугл-таблицы."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover(SHEET_SERVICE, SHEET_VERSION)
    spreadsheet_body = {
        'properties': {'title': f'Отчет на {now_date_time}',
                       'locale': settings.locale},
        'sheets': SHEETS
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle
) -> None:
    """Выдача прав аккаунту, указанному в core.config.settings."""
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover(DRIVE_SERVICE, DRIVE_VERSION)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: list[ProjectClosedDict],
    wrapper_services: Aiogoogle
) -> None:
    """Обновление данных в гугл-таблице."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover(SHEET_SERVICE, SHEET_VERSION)
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in projects:
        new_row = [
            project['name'],
            str(project['gathering_time']),
            project['description']
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'A1:C{len(table_values)}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
