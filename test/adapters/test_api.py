import random
import string

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from app.adapters.api import app
from app.domain.models import Tenant, Payment
from app.infrastructure.database import get_db

client = TestClient(app)

# Fixture de mock para la sesión de base de datos
@pytest.fixture
def mock_db_session():
    session_mock = MagicMock(spec=Session)
    app.dependency_overrides[get_db] = lambda: session_mock
    return session_mock

# Prueba de creación de pago con éxito
def test_create_payment_success(mock_db_session):
    # Configuración de datos de prueba para un pago exitoso

    random_code = random.randint(1000, 9999)
    payment_data = {
        "tenant_id_number": "123456",
        "property_code": "AB"+str(random_code),
        "paid_amount": 1000000,  # Simulando el pago completo de la renta
        "payment_date": "2024-10-11"
    }

    # Configura el mock para simular la existencia de un arrendatario en la base de datos
    mock_tenant = MagicMock()
    mock_db_session.query(Tenant).filter_by(tenant_id_number="123456").first.return_value = mock_tenant

    # Configura el mock para simular que no existen pagos duplicados para la misma propiedad y fecha
    mock_db_session.query(Payment).filter_by(
        property_code="AB"+str(random_code),
        payment_date="2024-10-11"
    ).first.return_value = None

    # Simula un commit exitoso
    mock_db_session.commit.return_value = None

    # Realiza la solicitud POST al endpoint de creación de pagos
    response = client.post("/api/payments", json=payment_data)

    # Imprime los detalles de la respuesta para análisis en caso de error
    print("Detalles de la respuesta:", response.status_code, response.text)  # Agrega esta línea para depuración

    # Verifica que el código de estado es 200 y el mensaje es el esperado
    assert response.status_code == 200, f"Se esperaba el código de estado 200, pero se recibió {response.status_code}"
    assert "Gracias por pagar su renta completa." in response.text, "El mensaje de éxito no coincide con el esperado."





# Prueba de listar pagos con éxito
def test_list_payments_success(mock_db_session):
    mock_db_session.query().all.return_value = [
        {
            "id": 1,
            "tenant_id_number": "123456",
            "property_code": "A1",
            "paid_amount": 500000,
            "payment_date": "2024-10-11"
        }
    ]

    response = client.get("/api/payments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

# Prueba de creación de arrendatario con éxito
def test_create_tenant_success(mock_db_session):
    random_id = random.randint(1000, 9999)
    random_email = ''.join(random.choices(string.ascii_letters, k=5))
    tenant_data = {
        "tenant_id_number": "12"+str(random_id),
        "full_name": "John Doe",
        "email": random_email+"@example.com",
        "phone": "123456789"
    }
    # Simula que el email no está en uso
    mock_db_session.query().filter_by().first.return_value = None

    response = client.post("/api/tenants", json=tenant_data)
    print(response.json())
    assert response.status_code == 200
    assert "Arrendatario registrado con éxito." in response.text

# Prueba de creación de arrendatario con email duplicado
def test_create_tenant_duplicate_email(mock_db_session):
    tenant_data = {
        "tenant_id_number": "123456",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789"
    }
    # Simula que el email ya está en uso
    mock_db_session.query().filter_by().first.return_value = MagicMock()

    response = client.post("/api/tenants", json=tenant_data)
    assert response.status_code == 400
    assert "Ya existe un arrendatario con este correo." in response.json()["detail"]

# Prueba de listar arrendatarios con éxito
def test_list_tenants_success(mock_db_session):
    mock_db_session.query().all.return_value = [
        {
            "tenant_id_number": "123456",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "phone": "123456789"
        }
    ]

    response = client.get("/api/tenants")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
