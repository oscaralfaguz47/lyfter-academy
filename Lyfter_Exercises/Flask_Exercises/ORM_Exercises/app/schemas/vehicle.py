from datetime import datetime

from pydantic import BaseModel, ConfigDict

class vehicleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    year: int
    status: str
    model_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime