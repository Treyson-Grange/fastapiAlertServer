from pydantic import BaseModel
from datetime import datetime

class Alert(BaseModel):
    message: str
    criticality: int
    autoClear: bool
    timestamp: datetime
    clearAfter: int
    group: str


class ManualAlert(BaseModel):
    dueDate: datetime
    daysNotice: int
    message: str
    group: str


class ApiAlerts(BaseModel):
    id: int = None
    type: str = "auto"
    message: str
    criticality: int
    timestamp: datetime
    days: int = None
