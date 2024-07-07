from pydantic import BaseModel,EmailStr
from typing import Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: Optional[str] = None
    company_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    mob: Optional[str] = None
    hashtag: Optional[str] = None
    date_of_birth: Optional[str] = None
    project_id: Optional[str] = None

class UserResponse(UserCreate):
    id: int

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    mob: Optional[str] = None
    hashtag: Optional[str] = None
    date_of_birth: Optional[str] = None
    username: Optional[str] = None
    project_id: Optional[str] = None