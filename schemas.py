# ensures correct data types for API requests
from pydantic import BaseModel

class FeedbackRequest(BaseModel):
    text: str
    model_prediction: int
    actual_label: int


class ReservationRequest(BaseModel):
    fullName: str
    email: str
    phone: str
    guests: str
    date: str
    time: str
    specialRequests: str | None = None
