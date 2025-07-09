# websocket_handler.py
from fastapi import WebSocket
import global_state
import asyncio
from repo_utils import detect_repo_info
from file_change_handler import file_change_queue  # Don't forget this!
from global_state import active_connections




async def connect_websocket(websocket: WebSocket):
    await websocket.accept()
    global_state.active_connections.add(websocket)
    print("🔌 WebSocket client connected.")

async def disconnect_websocket(websocket: WebSocket):
    global_state.active_connections.remove(websocket)
    print("❌ WebSocket client disconnected.")

async def broadcast_repo_info():
    while True:
        global_state.REPO_INFO = detect_repo_info()

        # Send latest to all connected clients
        for connection in active_connections:
            await connection.send_json(global_state.REPO_INFO)

        await asyncio.sleep(10)  # repeat every 10 seconds
        
async def send_to_all_clients(message: dict):
    for conn in active_connections:
        await conn.send_json(message)
        
# 4. New: Watch file change queue and broadcast events
async def file_change_broadcaster():
    print("📡 Starting file change broadcaster...")
    while True:
        ("📡 listed files:",global_state.CHANGED_FILES) 
        files = await file_change_queue.get()
        print("📡 Broadcasting files:", files)

    await send_to_all_clients({
    "event": "files_changed",
    "files": files,
    "message": f"You have {len(files)} uncommitted file(s). Don't forget to commit!"
    })


