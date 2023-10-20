from datetime import timedelta
from typing import TypedDict

ProjectClosedDict = TypedDict(
    'ProjectClosedDict',
    {'name': str,
     'gathering_time': timedelta,
     'description': str}
)
