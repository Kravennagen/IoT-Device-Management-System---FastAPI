from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import devices, firmware
from app.websockets import realtime
from app.services.mqtt_service import mqtt_service
from app.core.database import engine
from app.models import device

# Create database tables
device.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    mqtt_service.start()
    yield
    # Shutdown
    mqtt_service.stop()

app = FastAPI(
    title="IoT Device Management System",
    description="A comprehensive IoT device management platform with real-time monitoring",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(devices.router, prefix="/api/devices", tags=["devices"])
app.include_router(firmware.router, prefix="/api/firmware", tags=["firmware"])
app.include_router(realtime.router, prefix="/api", tags=["websockets"])

@app.get("/")
def read_root():
    return {
        "message": "IoT Device Management System API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}