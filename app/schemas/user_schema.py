from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional

class UserCreateSchema(BaseModel):
    email: EmailStr = Field(
        ...,
        description="User's email address",
        examples=["user@example.com"]
    )
    username: str = Field(
        ...,
        min_length=3,
        max_length=80,
        description="Unique username",
        examples=["john_doe"]
    )
    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="User password (will be hashed)",
        examples=["securePass123"]
    )
    first_name: Optional[str] = Field(
        None,
        max_length=50,
        description="User's first name",
        examples=["John"]
    )
    last_name: Optional[str] = Field(
        None,
        max_length=50,
        description="User's last name",
        examples=["Doe"]
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "email": "john@example.com",
                "username": "john_doe",
                "password": "secure123",
                "first_name": "John",
                "last_name": "Doe"
            }
        }
    )

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.isalnum() and '_' not in v:
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return v.lower()

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isalpha() for char in v):
            raise ValueError('Password must contain at least one letter')
        return v


class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr] = Field(None, description="New email address")
    username: Optional[str] = Field(None, min_length=3, max_length=80)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = Field(None, description="Account active status")

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "email": "newemail@example.com",
                "first_name": "Jane"
            }
        }
    )


class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)