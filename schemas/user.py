from uuid import UUID

from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic import Field

class User(BaseModel):
    id:  Optional[UUID]
    
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Loreali Gilmore"
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=60
    )
    email: EmailStr = Field(
        ...,
        example='lorelai@gmail.com' 
    )
    
