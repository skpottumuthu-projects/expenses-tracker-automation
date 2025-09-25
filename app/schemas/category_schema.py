from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
import re

class CategoryCreateSchema(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Category name",
        examples=["Food & Dining", "Transportation"]
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Category description",
        examples=["Restaurants, groceries, and food delivery"]
    )
    icon: Optional[str] = Field(
        None,
        max_length=50,
        description="Icon identifier or emoji",
        examples=["🍔", "food", "fa-utensils"]
    )
    color: Optional[str] = Field(
        None,
        pattern=r'^#[0-9A-Fa-f]{6}$',
        description="Hex color code",
        examples=["#FF5733", "#3498DB"]
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "name": "Food & Dining",
                "description": "Restaurant meals and groceries",
                "icon": "🍔",
                "color": "#FF5733"
            }
        }
    )

    @field_validator('color')
    @classmethod
    def validate_color(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not re.match(r'^#[0-9A-Fa-f]{6}$', v):
            raise ValueError('Color must be a valid hex code (e.g., #FF5733)')
        return v.upper()


class CategoryUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    icon: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(
        None,
        pattern=r'^#[0-9A-Fa-f]{6}$',
        description="Hex color code"
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "name": "Updated Category",
                "color": "#00FF00"
            }
        }
    )

    @field_validator('color')
    @classmethod
    def validate_color(cls, v: Optional[str]) -> Optional[str]:
        if v and not re.match(r'^#[0-9A-Fa-f]{6}$', v):
            raise ValueError('Color must be a valid hex code (e.g., #FF5733)')
        return v.upper() if v else v


class CategoryResponseSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    is_default: bool
    user_id: Optional[int] = None
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)