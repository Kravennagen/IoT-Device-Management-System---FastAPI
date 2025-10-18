import json
from typing import List, Dict, Any
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: Dict[str, Any]):
        message_str = json.dumps(message)
        for connection in self.active_connections:
            try:
                await connection.send_text(message_str)
            except:
                # Remove broken connections
                self.active_connections.remove(connection)
    
    async def broadcast_sensor_data(self, data: Dict[str, Any]):
        await self.broadcast({
            "type": "sensor_data",
            "data": data
        })
    
    async def broadcast_device_status(self, data: Dict[str, Any]):
        await self.broadcast({
            "type": "device_status",
            "data": data
        })
    
    async def broadcast_alert(self, data: Dict[str, Any]):
        await self.broadcast({
            "type": "alert",
            "data": data
        })

manager = ConnectionManager()