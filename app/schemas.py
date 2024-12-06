from pydantic import BaseModel
from datetime import datetime
from datetime import timezone


class Alert(BaseModel):
    # Descriptive message to be displayed in clients UI
    message: str

    # Criticality of the alert
    criticality: int

    # Whether or not the alert should be auto-cleared
    autoClear: bool

    # Initial timestamp of the alert
    timestamp: datetime = datetime.now(timezone.utc)

    # Time in minutes after which the alert should be auto-cleared
    clearAfter: int

    # Group to which the alert belongs (TODO: This should be a foreign key to a group)
    group: str


class ManualAlert(BaseModel):
    # Due date of the alert
    dueDate: datetime

    # Number of days before the due date that the alert should be displayed
    daysNotice: int

    # Descriptive message to be displayed in clients UI
    message: str

    # Group to which the alert belongs (TODO: This should be a foreign key to a group)
    group: str


class ApiAlerts(BaseModel):
    # ID of the alert
    id: int = None

    # Type of alert, either "auto" or "manual" corresponding to the above models
    type: str = "auto"

    # Descriptive message to be displayed in clients UI
    message: str

    # Criticality of the alert
    criticality: int

    # Initial timestamp of the alert
    timestamp: datetime


class Group(BaseModel):
    # Name of the group
    name: str

    # Description of the group (unused)
    description: str
