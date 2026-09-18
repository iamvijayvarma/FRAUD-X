from fastapi import WebSocket
from typing import List, Dict, Any
import json
import logging

logger = logging.getLogger("fraud_x.websocket")

class ConnectionManager:
    """Manages real-time WebSocket client connections and event broadcasting."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Total clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket client disconnected. Total clients: {len(self.active_connections)}")

    async def broadcast(self, event_type: str, data: Any):
        """Broadcasts structured event to all connected clients."""
        if not self.active_connections:
            return

        payload = {
            "type": event_type,
            "data": data
        }
        text = json.dumps(payload, default=str)

        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(text)
            except Exception as e:
                logger.warning(f"Failed to send to client ({e}); marking for removal.")
                disconnected.append(connection)

        for conn in disconnected:
            self.disconnect(conn)

manager = ConnectionManager()
