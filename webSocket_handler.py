# websocket_handler.py
from fastapi import WebSocket
import global_state
import asyncio
from repo_utils import detect_repo_info

active_connections = []

async def connect_websocket(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    print("🔌 WebSocket client connected.")

async def disconnect_websocket(websocket: WebSocket):
    active_connections.remove(websocket)
    print("❌ WebSocket client disconnected.")

async def broadcast_repo_info():
    while True:
        global_state.REPO_INFO = detect_repo_info()

        # Send latest to all connected clients
        for connection in active_connections:
            await connection.send_json(global_state.REPO_INFO)

        await asyncio.sleep(10)  # repeat every 10 seconds
