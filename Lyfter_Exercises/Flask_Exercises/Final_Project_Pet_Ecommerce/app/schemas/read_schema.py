""" How a complete read schema behaves. """
from pydantic import BaseModel, ConfigDict

class ReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)