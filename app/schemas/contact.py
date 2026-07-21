from pydantic import BaseModel, EmailStr, Field


class ContactFormRequest(BaseModel):
    firstName: str = Field(..., min_length=1, max_length=50)
    lastName: str = Field(..., min_length=1, max_length=50)
    address: str = Field(..., min_length=5, max_length=200)
    phone: str = Field(..., min_length=10, max_length=20)
    email: EmailStr
