from sqlalchemy.orm import Session
from datetime import datetime, date
from app.domain.models import Payment, Tenant
from fastapi import HTTPException

# Constantes para las reglas del negocio
RENT_AMOUNT = 1000000
DATE_FORMAT = "%Y-%m-%d"

def register_payment(session: Session, payment_data: dict):
    """
    Registra un pago para un arrendatario. Valida los datos del pago y aplica las reglas del negocio.

    Args:
        session (Session): Sesión de SQLAlchemy.
        payment_data (dict): Diccionario que contiene los datos del pago.

    Returns:
        str: Mensaje de éxito o aviso de pago parcial.
    """
    # Validar el formato de la fecha
    if isinstance(payment_data["payment_date"], str):
        try:
            payment_date = datetime.strptime(payment_data["payment_date"], DATE_FORMAT).date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use yyyy-mm-dd.")
    elif isinstance(payment_data["payment_date"], date):
        payment_date = payment_data["payment_date"]
    else:
        raise HTTPException(status_code=400, detail="Formato de fecha no reconocido.")

    # Validar que la fecha de pago sea un día impar
    if payment_date.day % 2 == 0:
        raise HTTPException(status_code=400, detail="Los pagos solo se aceptan en días impares.")

    # Validar que el documento de identificación del arrendatario sea numérico
    if not payment_data["tenant_id_number"].isdigit():
        raise HTTPException(status_code=400, detail="El documento de identificación del arrendatario debe ser numérico.")

    # Validar que el código de la propiedad sea alfanumérico
    if not payment_data["property_code"].isalnum():
        raise HTTPException(status_code=400, detail="El código de la propiedad debe ser alfanumérico.")

    # Validar el rango del monto del pago
    payment_amount = float(payment_data["paid_amount"])
    if payment_amount < 1 or payment_amount > RENT_AMOUNT:
        raise HTTPException(status_code=400, detail="El monto del pago debe estar entre 1 y 1,000,000.")

    # Verificar si el arrendatario existe
    tenant = session.query(Tenant).filter_by(
        tenant_id_number=payment_data["tenant_id_number"]
    ).first()

    if not tenant:
        raise HTTPException(status_code=404, detail="Arrendatario no encontrado.")

    # Verificar si ya existe un pago para la misma propiedad en la misma fecha
    existing_payment = session.query(Payment).filter_by(
        property_code=payment_data["property_code"],
        payment_date=payment_date
    ).first()

    if existing_payment:
        raise HTTPException(status_code=400, detail="Ya existe un pago registrado para esta propiedad en esta fecha.")

    # Registrar el pago
    new_payment = Payment(
        tenant_id_number=payment_data["tenant_id_number"],
        property_code=payment_data["property_code"],
        paid_amount=payment_amount,
        payment_date=payment_date
    )

    try:
        session.add(new_payment)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad: posible duplicación de datos.")


    # Determinar el mensaje apropiado basado en el monto del pago
    if payment_amount == RENT_AMOUNT:
        return "Gracias por pagar su renta completa."
    else:
        remaining_amount = RENT_AMOUNT - payment_amount
        return f"Gracias por su pago parcial. Sin embargo, aún debe ${remaining_amount}."


def get_payments(session: Session):
    """
    Recupera todos los pagos de la base de datos.

    Args:
        session (Session): Sesión de SQLAlchemy.

    Returns:
        list: Una lista de pagos.
    """
    payments = session.query(Payment).all()
    if not payments:  # Verificar si la lista de pagos está vacía
        raise HTTPException(status_code=404, detail="No hay pagos registrados aun.")
    return payments


def register_tenant(session: Session, tenant_data: dict):
    """
    Registra un nuevo arrendatario. Valida los datos del arrendatario y verifica el correo único.

    Args:
        session (Session): Sesión de SQLAlchemy.
        tenant_data (dict): Diccionario que contiene los datos del arrendatario.

    Returns:
        str: Mensaje de éxito.
    """
    # Verificar si el correo es único
    existing_tenant = session.query(Tenant).filter_by(
        email=tenant_data["email"]
    ).first()

    if existing_tenant:
        raise HTTPException(status_code=400, detail="Ya existe un arrendatario con este correo.")

    # Registrar el arrendatario
    new_tenant = Tenant(
        tenant_id_number=tenant_data["tenant_id_number"],
        full_name=tenant_data["full_name"],
        email=tenant_data["email"],
        phone=tenant_data["phone"]
    )
    session.add(new_tenant)
    session.commit()

    return "Arrendatario registrado con éxito."


def get_tenants(session: Session):
    """
    Recupera todos los arrendatarios de la base de datos.

    Args:
        session (Session): Sesión de SQLAlchemy.

    Returns:
        list: Una lista de arrendatarios.
    """
    tenants = session.query(Tenant).all()
    return tenants
