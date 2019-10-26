from fastapi import FastAPI
from pydantic import BaseModel, Schema
from nacl.utils import random as nacl_random
from nacl.public import PrivateKey, Box, SealedBox

from typing import List, Dict
from hashlib import new as new_hash
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

required = ...
optional = None

class User(BaseModel):
    _id: str = Schema(required, alias="Database ID", regex="^[0-9a-f]{32}$",
        description="Database ID")
    kind: str = Schema(required, alias="Kind", description="Kind of entry")
    name: str = Schema(required, alias="Name", description="Name of entry")
    time: int = Schema(required, alias="Timestamp", gt=0,
        description="UNIX timestamp of last update")
    uuid: str = Schema(required, alias="UUID",
        regex="^[a-zA-Z0-9_-]{42,44}={0,2}$", min_length=44, max_length=44,
        description="UUID of entry")
    pkey: str = Schema(required, alias="Public key",
        regex="^[a-zA-Z0-9_-]{42,44}={0,2}$", min_length=44, max_length=44,
        description="Public key of user")
    attr: Dict[str, str] = Schema(required, alias="Attributes",
        description="Key is the relationship, value is the attribute UUID")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, world!"}

@app.get("/users")
async def users_schema():
    return User.schema()

@app.get("/users/{user_uuid}")
def get_user(user_uuid: str, q: str = None):
    return {"user_uuid": user_uuid, "q": q}


@app.put("/users/{user_uuid}")
def update_user(user_uuid: str, user: User):
    res = dict()
    res["_id"] = user._id
    res["type"] = user.type
    res["name"] = user.name
    res["uuid"] = user.uuid
    res["pkey"] = user.pkey
    res["attr"] = user.attr
    return res
