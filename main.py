from fastapi import FastAPI,WebSocket
from git_handler import pull_code,commit_code,push_code
from db import init_db, save_github_credentials, get_github_credentials
from pydantic import BaseModel
from repo_utils import detect_repo_info
import global_state
from webSocket_handler import connect_websocket, disconnect_websocket, broadcast_repo_info,file_change_broadcaster
import asyncio
from file_watcher import start_file_watcher
import threading


app = FastAPI()
init_db()
class AuthRequest(BaseModel):
    username: str
    token: str

@app.post("/auth")
def auth(auth: AuthRequest):
	save_github_credentials(auth.username, auth.token)
	return {"message": "GitHub credentials saved successfully."}

@app.get("/home")
def home():
	return{"message":"Welocme to GIT AI AGENT Buddy"}

@app.get("/pull")
def pull():
	result=pull_code()  #returns in json format 
	return result  

@app.get("/commit")
def commit(issue_description: str,mode):  
    result = commit_code(issue_description,mode)
    return result

@app.get("/push")
def push():  
    result = push_code()
    return result

@app.on_event("startup")
async def startup_event():
    global_state.REPO_INFO = detect_repo_info()
    print("🧠 Repo info detected on startup:", global_state.REPO_INFO)

    asyncio.create_task(broadcast_repo_info())
    asyncio.create_task(file_change_broadcaster())
    
    
    loop = asyncio.get_running_loop()
    threading.Thread(target=start_file_watcher, args=(loop,), daemon=True).start()
    
   

@app.websocket("/ws/repo-info")
async def websocket_endpoint(websocket: WebSocket):
    await connect_websocket(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep alive
    except:
        await disconnect_websocket(websocket)
