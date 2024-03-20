from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4


class Pet(BaseModel):
    id: Optional[UUID] = uuid4()
    name: str
    favorite_delicacy: str
    weight: int
    age: int
    favorite_activity: str