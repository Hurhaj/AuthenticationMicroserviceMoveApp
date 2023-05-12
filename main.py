import os
from datetime import datetime, timezone

import jwt
import requests
import uvicorn
from fastapi import FastAPI
from google.auth.transport import requests
from google.oauth2 import id_token
from pydantic import BaseModel


class Authenticated(BaseModel):
    email: str
    error: bool


# load environment variables
port = os.environ["PORT"]
# initialize FastAPI
app = FastAPI()


@app.get("/")
def index():
    return {"data": "Application ran successfully - authentication microservice is working! Also, its deployed!"}


@app.post("/hello")
def hello():
    return {"hello": "world"}


@app.post("/authenticate")
def authenticate(token: str):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(),
                                              "168397874560-5uso2lk8p5pa43h3sb3eg9futfisese0.apps.googleusercontent.com")
        expiration_time = datetime.fromtimestamp(idinfo['exp'], timezone.utc)
        if datetime.now(timezone.utc) >= expiration_time:
            return Authenticated(email="token expired", error=True)
        return Authenticated(email=idinfo["email"], error=False)
    except jwt.exceptions.InvalidSignatureError:
        return Authenticated(email="Invalid_token_error", error=True)
    except jwt.exceptions.DecodeError:
        return Authenticated(email="Decode_error", error=True)
    except jwt.exceptions.InvalidTokenError:
        return Authenticated(email="Invalid_token_error", error=True)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
