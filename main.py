import os
from datetime import datetime, timezone

import requests
import uvicorn
from fastapi import FastAPI
from google.auth.transport import requests
from google.oauth2 import id_token
from pydantic import BaseModel


class Authenticated(BaseModel):
    msg: str
    error: bool


# load environment variables

# initialize FastAPI
app = FastAPI()


@app.get("/")
def index():
    return {"data": "Application ran successfully - authentication, should be working! version : v0.0.1"}


@app.get("/hello")
def hello():
    return {"hello": "world"}


@app.post("/authenticate")
async def authenticate(token: str):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(),
                                          "168397874560-5uso2lk8p5pa43h3sb3eg9futfisese0.apps.googleusercontent.com")
        return Authenticated(msg=idinfo["email"], error=False)
    except Exception as e:
        return Authenticated(msg=str(e), error=True)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
