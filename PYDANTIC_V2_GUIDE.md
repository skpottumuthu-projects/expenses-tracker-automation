# Pydantic V2 Complete Guide

## What Changed from V1 to V2?

### 1. **Field() - Enhanced Field Definition**

**Old Way (V1):**
```python
from pydantic import BaseModel

class User(BaseModel):
    username: str
    age: int
```

**New Way (V2):**
```python
from pydantic import BaseModel, Field

class User(BaseModel):
    username: str = Field(
        ...,  # Required field (replaces default=...)
        min_length=3,
        max_length=50,
        description="User's unique username",
        examples=["john_doe"]
    )
    age: int = Field(..., ge=0, le=120, description="User's age")
```

**Key Features:**
- `...` = Required field
- `min_length`, `max_length` = String constraints
- `gt`, `ge`, `lt`, `le` = Numeric constraints (greater than, greater/equal, etc.)
- `decimal_places` = Decimal precision
- `pattern` = Regex validation
- `examples` = Example values for docs
- `description` = Field documentation

---

### 2. **ConfigDict - Model Configuration**

**Old Way (V1):**
```python
class User(BaseModel):
    class Config:
        orm_mode = True
        str_strip_whitespace = True
```

**New Way (V2):**
```python
from pydantic import ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,  # Replaces orm_mode
        str_strip_whitespace=True,
        validate_assignment=True,
        json_schema_extra={
            "example": {"username": "john_doe"}
        }
    )
```

**Common Config Options:**
- `from_attributes=True` - Enable ORM/dataclass support
- `str_strip_whitespace=True` - Auto-trim strings
- `validate_assignment=True` - Validate on attribute assignment
- `json_schema_extra` - Add examples to schema
- `populate_by_name=True` - Allow field aliases

---

### 3. **field_validator - Custom Validation**

**Syntax:**
```python
from pydantic import field_validator

class User(BaseModel):
    username: str

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v.lower()  # Transform and return
```

**Key Points:**
- Must be a `@classmethod`
- First param is `cls`, second is value `v`
- Must return the value (transformed or original)
- Can validate multiple fields: `@field_validator('field1', 'field2')`

**Accessing Other Fields (V2):**
```python
@field_validator('end_date')
@classmethod
def validate_end_date(cls, v: datetime, info) -> datetime:
    # Access other fields via info.data
    if v and info.data.get('start_date') and v <= info.data['start_date']:
        raise ValueError('End date must be after start date')
    return v
```

---

### 4. **Literal Types - Enums Made Easy**

**Old Way:**
```python
from enum import Enum

class PaymentMethod(str, Enum):
    CASH = "cash"
    CARD = "card"
```

**New Way (V2):**
```python
from typing import Literal

PaymentMethod = Literal['cash', 'credit_card', 'debit_card', 'other']

class Expense(BaseModel):
    payment_method: PaymentMethod  # Auto-validates!
```

**Benefits:**
- No enum class needed
- Auto-validates against allowed values
- Better type hints
- Works great with OpenAPI/JSON Schema

---

### 5. **Response Schemas - ORM Integration**

**Pattern:**
```python
class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)
```

**Usage:**
```python
# In your controller
user = User.query.get(1)  # SQLAlchemy model
return UserResponseSchema.model_validate(user)  # Auto-converts!
```

**Why `from_attributes=True`?**
- Reads from object attributes (not just dict)
- Works with SQLAlchemy models, dataclasses, etc.
- Old V1 name: `orm_mode = True`

---

## 🎯 Real-World Examples from Our Code

### Example 1: User Schema with Advanced Validation

```python
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict

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
        description="Unique username"
    )
    password: str = Field(
        ...,
        min_length=6,
        description="User password"
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "email": "john@example.com",
                "username": "john_doe",
                "password": "secure123"
            }
        }
    )

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.isalnum() and '_' not in v:
            raise ValueError('Username: letters, numbers, _ only')
        return v.lower()

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(c.isdigit() for c in v):
            raise ValueError('Password needs 1+ digit')
        if not any(c.isalpha() for c in v):
            raise ValueError('Password needs 1+ letter')
        return v
```

**What's happening:**
1. **EmailStr** - Auto-validates email format
2. **Field()** - Adds min/max length, descriptions, examples
3. **ConfigDict** - Strips whitespace, adds schema examples
4. **field_validator** - Custom logic (alphanumeric check, password strength)
5. Returns transformed value (`.lower()`)

---

### Example 2: Expense Schema with Decimal & Datetime

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime
from decimal import Decimal

PaymentMethod = Literal['cash', 'credit_card', 'debit_card', 'other']

class ExpenseCreateSchema(BaseModel):
    amount: Decimal = Field(
        ...,
        gt=0,  # Greater than 0
        decimal_places=2,
        description="Expense amount",
        examples=[50.00, 123.45]
    )
    description: str = Field(
        ...,
        min_length=1,
        max_length=200
    )
    expense_date: Optional[datetime] = Field(
        None,
        description="Defaults to now"
    )
    payment_method: Optional[PaymentMethod] = None

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        if v > Decimal('999999.99'):
            raise ValueError('Amount too large')
        return round(v, 2)

    @field_validator('expense_date')
    @classmethod
    def validate_date(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v and v > datetime.now():
            raise ValueError('Cannot be future date')
        return v
```

**Key Learnings:**
1. **Decimal** - Use for money (not float!)
2. **gt=0** - Greater than constraint
3. **decimal_places=2** - Enforce 2 decimal places
4. **Literal** - Restrict to specific values
5. **Optional** - Field can be None
6. **Validation** - Check max value, future dates

---

### Example 3: Budget Schema with Cross-Field Validation

```python
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Literal, Optional
from datetime import datetime
from decimal import Decimal

BudgetPeriod = Literal['daily', 'weekly', 'monthly', 'yearly']

class BudgetCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    period: BudgetPeriod
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    alert_threshold: int = Field(80, ge=1, le=100)

    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v: Optional[datetime], info) -> Optional[datetime]:
        # Access other field values via info.data
        start = info.data.get('start_date')
        if v and start and v <= start:
            raise ValueError('End date must be after start date')
        return v
```

**Cross-Field Validation:**
- Use `info.data.get('field_name')` to access other fields
- Validates relationships between fields
- Only works with fields defined BEFORE current field

---

### Example 4: Category Schema with Regex Pattern

```python
from pydantic import BaseModel, Field, field_validator
import re

class CategoryCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    color: Optional[str] = Field(
        None,
        pattern=r'^#[0-9A-Fa-f]{6}$',  # Hex color regex
        description="Hex color code",
        examples=["#FF5733"]
    )

    @field_validator('color')
    @classmethod
    def validate_color(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not re.match(r'^#[0-9A-Fa-f]{6}$', v):
            raise ValueError('Invalid hex color (e.g., #FF5733)')
        return v.upper()  # Normalize to uppercase
```

**Pattern Matching:**
- `pattern=r'...'` - Regex in Field()
- `field_validator` - Extra custom logic
- Return transformed value (`.upper()`)

---

## 📋 Best Practices Checklist

### ✅ Always Use:
1. **Field()** for all fields with constraints
2. **ConfigDict** for model configuration
3. **Literal** instead of Enum when possible
4. **Decimal** for money/currency
5. **EmailStr** for emails
6. **HttpUrl** for URLs
7. **from_attributes=True** for ORM models

### ✅ Naming Conventions:
- `*CreateSchema` - For POST requests
- `*UpdateSchema` - For PUT/PATCH requests (all Optional)
- `*ResponseSchema` - For API responses

### ✅ Validation Tips:
- **Field constraints first** - Use Field(min_length=..., gt=...)
- **@field_validator second** - For complex logic
- **Return transformed values** - Normalize data
- **Type hints everywhere** - `v: str`, `-> str`

### ✅ Documentation:
- Add `description` to every field
- Add `examples` for clarity
- Use `json_schema_extra` for complete examples

---

## 🚀 Quick Reference Card

```python
# Imports
from pydantic import (
    BaseModel,
    Field,
    field_validator,
    ConfigDict,
    EmailStr,
    HttpUrl
)
from typing import Optional, Literal
from decimal import Decimal
from datetime import datetime

# Required field
name: str = Field(...)

# Optional field
description: Optional[str] = Field(None)

# String constraints
username: str = Field(..., min_length=3, max_length=50)

# Numeric constraints
age: int = Field(..., ge=0, le=120)
price: Decimal = Field(..., gt=0, decimal_places=2)

# Regex pattern
color: str = Field(..., pattern=r'^#[0-9A-Fa-f]{6}$')

# Literal (enum replacement)
status: Literal['active', 'inactive', 'pending']

# Custom validation
@field_validator('email')
@classmethod
def validate_email(cls, v: str) -> str:
    return v.lower()

# Config
model_config = ConfigDict(
    from_attributes=True,
    str_strip_whitespace=True
)
```

---

## 🔥 Common Gotchas

1. **Don't forget `@classmethod`** on validators
2. **Always return the value** from validators
3. **Use `info.data`** for cross-field validation
4. **`from_attributes=True`** for SQLAlchemy models
5. **Decimal not float** for money
6. **Optional vs default value** - `None` means optional

---

## Summary

**Pydantic V2 = Type Safety + Data Validation + Auto Documentation**

Our schemas now have:
- ✅ Strict type checking
- ✅ Automatic validation
- ✅ Clear error messages
- ✅ API documentation (OpenAPI/Swagger ready)
- ✅ Data transformation
- ✅ ORM integration

**Next Steps:**
1. Test with invalid data to see error messages
2. Generate OpenAPI docs (Flask-RESTX or similar)
3. Add more validators as business rules grow