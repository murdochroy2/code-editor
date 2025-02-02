from typing import Dict, Set
from fastapi import WebSocket
import json
from app.models.user import User

class ConnectionManager:
    def __init__(self):
        # file_id -> set of WebSocket connections
        self.active_connections: Dict[int, Dict[int, WebSocket]] = {}
        # file_id -> Dict[user_id -> cursor_position]
        self.cursor_positions: Dict[int, Dict[int, int]] = {}
    
    async def connect(self, websocket: WebSocket, file_id: int, user_id: int):
        await websocket.accept()
        if file_id not in self.active_connections:
            self.active_connections[file_id] = {}
            self.cursor_positions[file_id] = {}
        
        self.active_connections[file_id][user_id] = websocket
        
    async def disconnect(self, file_id: int, user_id: int):
        if file_id in self.active_connections:
            self.active_connections[file_id].pop(user_id, None)
            self.cursor_positions[file_id].pop(user_id, None)
            
            if not self.active_connections[file_id]:
                del self.active_connections[file_id]
                del self.cursor_positions[file_id]
    
    async def update_cursor(self, file_id: int, user_id: int, position: int):
        if file_id in self.cursor_positions:
            self.cursor_positions[file_id][user_id] = position
            await self.broadcast_cursors(file_id)
    
    async def broadcast_cursors(self, file_id: int):
        if file_id in self.active_connections:
            for connection in self.active_connections[file_id].values():
                await connection.send_json({
                    "type": "cursor_update",
                    "cursors": self.cursor_positions[file_id]
                })
    
    async def broadcast_code_update(self, file_id: int, content: str, user_id: int):
        if file_id in self.active_connections:
            for conn_user_id, connection in self.active_connections[file_id].items():
                if conn_user_id != user_id:  # Don't send back to sender
                    await connection.send_json({
                        "type": "code_update",
                        "content": content,
                        "user_id": user_id
                    })

manager = ConnectionManager() 