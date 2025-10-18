# IoT Device Management System

A comprehensive FastAPI-based IoT device management platform with real-time monitoring, MQTT integration, and WebSocket support.

## Features

- **Device Management**: Register, monitor, and manage IoT devices
- **Real-time Data**: Live sensor data collection via MQTT
- **WebSocket Support**: Real-time updates to connected clients
- **Alert System**: Automated alerts and notifications
- **Firmware Management**: OTA firmware update capabilities
- **Time-series Data**: Historical sensor data storage and retrieval
- **RESTful API**: Comprehensive REST API with OpenAPI documentation

## Tech Stack

- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM with PostgreSQL
- **MQTT**: IoT device communication protocol
- **WebSockets**: Real-time client communication
- **Redis**: Caching and session management
- **Docker**: Containerization and deployment
- **Pytest**: Unit and integration testing

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Clone and navigate to project
cd fastapi_project

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f app
```

### Manual Setup

```bash
# Install dependencies
pipenv install --dev

# Set environment variables
export DATABASE_URL="postgresql://user:password@localhost/iot_db"
export REDIS_URL="redis://localhost:6379"
export MQTT_BROKER="localhost"

# Run the application
uvicorn app.main:app --reload
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Key Endpoints

### Device Management
- `POST /api/devices/` - Register new device
- `GET /api/devices/` - List all devices
- `GET /api/devices/{device_id}` - Get device details
- `PUT /api/devices/{device_id}` - Update device
- `DELETE /api/devices/{device_id}` - Remove device

### Sensor Data
- `POST /api/devices/{device_id}/sensor-data` - Add sensor reading
- `GET /api/devices/{device_id}/sensor-data` - Get historical data

### Alerts
- `POST /api/devices/{device_id}/alerts` - Create alert
- `GET /api/devices/{device_id}/alerts` - Get device alerts
- `PUT /api/alerts/{alert_id}/resolve` - Resolve alert

### Firmware Management
- `POST /api/firmware/` - Upload firmware update
- `GET /api/firmware/` - List firmware versions
- `POST /api/firmware/{firmware_id}/deploy/{device_id}` - Deploy update

### Real-time Communication
- `WebSocket /api/ws` - Real-time updates

## MQTT Topics

The system listens to these MQTT topics:

- `devices/{device_id}/data` - Sensor data
- `devices/{device_id}/status` - Device status updates
- `devices/{device_id}/alerts` - Device alerts
- `devices/{device_id}/commands` - Commands to devices

## Example Device Data

### Sensor Data Message
```json
{
  "sensor_type": "temperature",
  "value": 23.5,
  "unit": "celsius",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Device Status Message
```json
{
  "status": "online",
  "firmware_version": "1.2.0",
  "battery_level": 85
}
```

### Alert Message
```json
{
  "alert_type": "temperature_high",
  "message": "Temperature exceeded threshold",
  "severity": "warning"
}
```

## Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=app tests/
```

## Development

### Project Structure
```
app/
├── api/           # API route handlers
├── core/          # Core configuration
├── models/        # Database models
├── schemas/       # Pydantic schemas
├── services/      # Business logic services
├── websockets/    # WebSocket handlers
└── main.py        # Application entry point
```

### Adding New Features

1. Create database models in `app/models/`
2. Define Pydantic schemas in `app/schemas/`
3. Implement business logic in `app/services/`
4. Create API endpoints in `app/api/`
5. Add tests in `tests/`

## Deployment

### Production Considerations

- Use environment variables for sensitive configuration
- Set up proper database migrations with Alembic
- Configure reverse proxy (nginx) for production
- Set up monitoring and logging
- Use Redis for session management and caching
- Implement rate limiting and authentication

### Environment Variables

```bash
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://host:port
MQTT_BROKER=mqtt.broker.com
MQTT_PORT=1883
SECRET_KEY=your-secret-key
```

## Portfolio Highlights

This project demonstrates:

- **Scalable Architecture**: Microservices-ready design
- **Real-time Systems**: WebSocket and MQTT integration
- **Database Design**: Proper relationships and indexing
- **API Design**: RESTful principles with comprehensive documentation
- **Testing**: Unit and integration test coverage
- **DevOps**: Docker containerization and orchestration
- **IoT Integration**: MQTT protocol and device management
- **Performance**: Async/await patterns and caching strategies

## License

MIT License - feel free to use this project as a portfolio piece or learning resource.