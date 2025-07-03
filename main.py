from fastapi import FastAPI
from git_handler import pull_code
from db import init_db, save_github_credentials, get_github_credentials
from pydantic import BaseModel

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

	