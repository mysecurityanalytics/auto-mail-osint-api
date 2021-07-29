from fastapi import FastAPI
from pydantic import BaseModel
import pymongo, bcrypt, jwt
from modules.verify import Verify
import os

db_url = os.environ.get("DATABASE_URL")
client = pymongo.MongoClient(db_url)
db = os.environ.get("DB_NAME")
users_col = client[db]["users"]


class user(BaseModel):
    email: str
    password: str


jwt_secret = str(os.environ.get("JWT_SECRET"))


auth = FastAPI(openapi_prefix="/auth")


@auth.post("/login/")
async def login(user: user):
    e = await Verify(user.email).check_regex()
    if not e:
        return {"status": "failed", "message": "Wrong email format!"}
    check = {"email": user.email}
    if users_col.count_documents(check):
        data = users_col.find_one({"email": user.email})
        bcrypt_pass = str.encode(user.password)
        hashed = data["password"]
        if bcrypt.checkpw(bcrypt_pass, hashed):
            token = jwt.encode({"email": user.email}, jwt_secret, algorithm="HS256")
            return {"status": "success", "token": token}
        else:
            return {"status": "failed", "message": "Incorrect username or password!"}
    else:
        return {"status": "failed", "message": "Incorrect username or password!"}


@auth.post("/register/")
async def register(user: user):
    e = await Verify(user.email).check_regex()
    if not e:
        return {"status": "failed", "message": "Wrong email format!"}
    check = {"email": user.email}
    if users_col.count_documents(check):
        return {"status": "failed", "message": "Email already taken!"}
    else:
        bcrypt_pass = str.encode(user.password)
        hashed = bcrypt.hashpw(bcrypt_pass, bcrypt.gensalt())
        q = {"email": user.email, "password": hashed}
        x = users_col.insert_one(q)
        return {"status": "success", "message": "Success!"}
