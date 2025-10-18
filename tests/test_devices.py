import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db, Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.mark.parametrize("device_data,expected_status", [
    ({
        "device_id": "test_device_001",
        "name": "Test Temperature Sensor",
        "device_type": "temperature_sensor",
        "firmware_version": "1.0.0"
    }, 200),
    ({
        "device_id": "test_device_002",
        "name": "Test Humidity Sensor",
        "device_type": "humidity_sensor"
    }, 200),
    ({
        "device_id": "",
        "name": "Invalid Device",
        "device_type": "temperature_sensor"
    }, 422)
])
def test_create_device(device_data, expected_status):
    response = client.post("/api/devices/", json=device_data)
    assert response.status_code == expected_status
    if expected_status == 200:
        data = response.json()
        assert data["device_id"] == device_data["device_id"]
        assert data["name"] == device_data["name"]

@pytest.mark.parametrize("query_params,expected_status", [
    ({}, 200),
    ({"status": "online"}, 200),
    ({"device_type": "temperature_sensor"}, 200),
    ({"limit": 10}, 200)
])
def test_get_devices(query_params, expected_status):
    response = client.get("/api/devices/", params=query_params)
    assert response.status_code == expected_status
    assert isinstance(response.json(), list)

@pytest.mark.parametrize("sensor_data,expected_status", [
    ({
        "device_id": "sensor_test_001",
        "sensor_type": "temperature",
        "value": 23.5,
        "unit": "celsius"
    }, 200),
    ({
        "device_id": "sensor_test_001",
        "sensor_type": "humidity",
        "value": 65.0,
        "unit": "percent"
    }, 200),
    ({
        "device_id": "nonexistent_device",
        "sensor_type": "temperature",
        "value": 25.0
    }, 404)
])
def test_add_sensor_data(sensor_data, expected_status):
    # Create device first for valid tests
    if expected_status == 200:
        client.post("/api/devices/", json={
            "device_id": sensor_data["device_id"],
            "name": "Test Sensor",
            "device_type": "temperature_sensor"
        })
    
    response = client.post(
        f"/api/devices/{sensor_data['device_id']}/sensor-data",
        json=sensor_data
    )
    assert response.status_code == expected_status
    if expected_status == 200:
        data = response.json()
        assert data["value"] == sensor_data["value"]
        assert data["sensor_type"] == sensor_data["sensor_type"]