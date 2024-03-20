from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4


class Password(BaseModel):
    id: Optional[UUID] = uuid4()
    password: str
    password_type: str