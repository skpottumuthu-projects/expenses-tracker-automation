from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, Literal
from datetime import datetime
from decimal import Decimal

BudgetPeriod = Literal['daily', 'weekly', 'monthly', 'yearly']

class BudgetCreateSchema(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Budget name",
        examples=["Monthly Food Budget", "Weekly Transport"]
    )
    amount: Decimal = Field(
        ...,
        gt=0,
        decimal_places=2,
        description="Budget limit amount",
        examples=[500.00, 1000.00]
    )
    period: BudgetPeriod = Field(
        ...,
        description="Budget period",
        examples=["monthly", "weekly"]
    )
    start_date: Optional[datetime] = Field(
        None,
        description="Budget start date (defaults to now)",
        examples=["2024-01-01T00:00:00"]
    )
    end_date: Optional[datetime] = Field(
        None,
        description="Budget end date (null for ongoing)",
        examples=["2024-12-31T23:59:59"]
    )
    alert_threshold: int = Field(
        80,
        ge=1,
        le=100,
        description="Alert when usage reaches this percentage",
        examples=[80, 90]
    )
    category_id: Optional[int] = Field(
        None,
        gt=0,
        description="Category ID (null for overall budget)",
        examples=[1, None]
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "name": "Monthly Food Budget",
                "amount": 500.00,
                "period": "monthly",
                "start_date": "2024-01-01T00:00:00",
                "alert_threshold": 80,
                "category_id": 1
            }
        }
    )

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        if v > Decimal('9999999.99'):
            raise ValueError('Amount cannot exceed 9,999,999.99')
        return round(v, 2)

    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v: Optional[datetime], info) -> Optional[datetime]:
        if v and info.data.get('start_date') and v <= info.data['start_date']:
            raise ValueError('End date must be after start date')
        return v


class BudgetUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    amount: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    period: Optional[BudgetPeriod] = None
    end_date: Optional[datetime] = None
    alert_threshold: Optional[int] = Field(None, ge=1, le=100)
    is_active: Optional[bool] = Field(
        None,
        description="Set to false to pause budget tracking"
    )
    category_id: Optional[int] = Field(None, gt=0)

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "amount": 600.00,
                "alert_threshold": 75,
                "is_active": True
            }
        }
    )

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        if v is not None and v <= 0:
            raise ValueError('Amount must be greater than 0')
        return round(v, 2) if v else v


class BudgetResponseSchema(BaseModel):
    id: int
    name: str
    amount: Decimal
    period: str
    start_date: datetime
    end_date: Optional[datetime] = None
    alert_threshold: int
    is_active: bool
    user_id: int
    category_id: Optional[int] = None
    spent_amount: float
    remaining_amount: float
    usage_percentage: float
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)