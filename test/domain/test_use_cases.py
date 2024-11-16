import random

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from app.adapters.api import app
from app.domain.models import Payment, Tenant
from app.infrastructure.database import get_db


client = TestClient(app)

# Mock de la dependencia de la base de datos
@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)

# Sobrescribimos la dependencia de get_db para usar el mock en las pruebas
app.dependency_overrides[get_db] = lambda: mock_db_session

def test_create_payment_success(mock_db_session):
    random_code = random.randint(1000, 9000)
    payment_data = {
        "tenant_id_number": "123456",
        "property_code": "AB"+str(random_code),
        "paid_amount": 1000000,
        "payment_date": "2024-10-11"
    }

    mock_tenant = MagicMock()
    mock_db_session.query(Tenant).filter_by(tenant_id_number="123456").first.return_value = mock_tenant
    mock_db_session.query(Payment).filter_by(
        property_code="AB" + str(random_code),
        payment_date="2024-10-11"
    ).first.return_value = None

    mock_db_session.commit.return_value = None

    response = client.post("/api/payments", json=payment_data)
    print('hi'+response.json())

    assert response.status_code == 200
    assert response.json() == "Gracias por pagar su renta completa."


def test_create_payment_even_day(mock_db_session):
    payment_data = {
        "tenant_id_number": "123456",
        "property_code": "A1",
        "paid_amount": 500000,
        "payment_date": "2024-10-10"  # Día par
    }

    response = client.post("/api/payments", json=payment_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Los pagos solo se aceptan en días impares."



