from pydantic import BaseModel, Field, field_validator, HttpUrl, ConfigDict
from typing import Optional, Literal
from datetime import datetime
from decimal import Decimal

PaymentMethod = Literal['cash', 'credit_card', 'debit_card', 'bank_transfer', 'digital_wallet', 'other']

class ExpenseCreateSchema(BaseModel):
    amount: Decimal = Field(
        ...,
        gt=0,
        decimal_places=2,
        description="Expense amount (must be positive)",
        examples=[50.00, 123.45]
    )
    description: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Brief description of expense",
        examples=["Lunch at restaurant", "Uber ride to office"]
    )
    notes: Optional[str] = Field(
        None,
        max_length=1000,
        description="Additional notes or details",
        examples=["Team lunch with 5 people"]
    )
    expense_date: Optional[datetime] = Field(
        None,
        description="Date and time of expense (defaults to now)",
        examples=["2024-01-15T12:30:00"]
    )
    payment_method: Optional[PaymentMethod] = Field(
        None,
        description="Method of payment",
        examples=["credit_card", "cash"]
    )
    receipt_url: Optional[str] = Field(
        None,
        max_length=500,
        description="URL to receipt image/file",
        examples=["https://example.com/receipts/123.jpg"]
    )
    category_id: int = Field(
        ...,
        gt=0,
        description="Category ID for this expense",
        examples=[1, 5]
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "amount": 50.00,
                "description": "Lunch at restaurant",
                "notes": "Team lunch",
                "expense_date": "2024-01-15T12:30:00",
                "payment_method": "credit_card",
                "category_id": 1
            }
        }
    )

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        if v > Decimal('999999.99'):
            raise ValueError('Amount cannot exceed 999,999.99')
        return round(v, 2)

    @field_validator('expense_date')
    @classmethod
    def validate_expense_date(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v and v > datetime.now():
            raise ValueError('Expense date cannot be in the future')
        return v


class ExpenseUpdateSchema(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    description: Optional[str] = Field(None, min_length=1, max_length=200)
    notes: Optional[str] = Field(None, max_length=1000)
    expense_date: Optional[datetime] = None
    payment_method: Optional[PaymentMethod] = None
    receipt_url: Optional[str] = Field(None, max_length=500)
    category_id: Optional[int] = Field(None, gt=0)

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "amount": 55.00,
                "description": "Updated expense"
            }
        }
    )

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        if v is not None and v <= 0:
            raise ValueError('Amount must be greater than 0')
        return round(v, 2) if v else v


class ExpenseResponseSchema(BaseModel):
    id: int
    amount: Decimal
    description: str
    notes: Optional[str] = None
    expense_date: datetime
    payment_method: Optional[str] = None
    receipt_url: Optional[str] = None
    user_id: int
    category_id: int
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)