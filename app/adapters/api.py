
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.domain.use_cases import register_payment, get_payments, register_tenant, get_tenants
from app.infrastructure.database import SessionLocal
from app.domain.schemas import PaymentCreate, PaymentResponse, TenantCreate, TenantResponse
from typing import List

app = FastAPI()

# Dependency to get the SQLAlchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/payments", response_model=str)
async def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new payment.
    """
    response = register_payment(db, payment.model_dump())
    return response

@app.get("/api/payments", response_model=List[PaymentResponse])
async def list_payments(db: Session = Depends(get_db)):
    """
    Endpoint to get a list of all payments.
    """
    payments = get_payments(db)
    return payments

@app.post("/api/tenants", response_model=str)
async def create_tenant(tenant: TenantCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new tenant.
    """
    response = register_tenant(db, tenant.model_dump())
    return response

@app.get("/api/tenants", response_model=List[TenantResponse])
async def list_tenants(db: Session = Depends(get_db)):
    """
    Endpoint to get a list of all tenants.
    """
    tenants = get_tenants(db)
    return tenants
