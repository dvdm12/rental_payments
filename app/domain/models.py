from sqlalchemy import Column, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base


# Modelo de arrendatarios
class Tenant(Base):
    __tablename__ = "tenants"
    tenant_id_number = Column(String, primary_key=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)


# Modelo de pagos
class Payment(Base):
    __tablename__ = "payments"
    property_code = Column(String, primary_key=True)
    tenant_id_number = Column(String, ForeignKey('tenants.tenant_id_number'), nullable=False)
    paid_amount = Column(Numeric)
    payment_date = Column(Date)

    tenant = relationship("Tenant")
