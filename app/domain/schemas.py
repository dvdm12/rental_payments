from pydantic import BaseModel, EmailStr, condecimal
from datetime import date
from typing import Optional

class PaymentCreate(BaseModel):
    tenant_id_number: str
    property_code: str
    paid_amount: condecimal(max_digits=10, decimal_places=2)
    payment_date: date

    class Config:
        from_attributes = True


class PaymentResponse(BaseModel):
    tenant_id_number: str
    property_code: str
    paid_amount: condecimal(max_digits=10, decimal_places=2)
    payment_date: date

    class Config:
        from_attributes = True


class TenantCreate(BaseModel):
    tenant_id_number: str
    full_name: str
    email: EmailStr
    phone: str

    class Config:
        from_attributes = True


class TenantResponse(BaseModel):
    tenant_id_number: str
    full_name: str
    email: EmailStr
    phone: str

    class Config:
        from_attributes = True
