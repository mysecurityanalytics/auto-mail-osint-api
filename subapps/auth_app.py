from fastapi import FastAPI
from pydantic import BaseModel
import pymongo, bcrypt, jwt, os
from modules.verify import Verify
from fastapi.responses import JSONResponse
import time

db_url = os.environ.get("DATABASE_URL")
client = pymongo.MongoClient(db_url)
db = os.environ.get("DB_NAME")
users_col = client[db]["users"]
login_logs_col = client[db]["login_logs"]


class user(BaseModel):
    email: str
    password: str


jwt_secret = str(os.environ.get("JWT_SECRET"))


auth = FastAPI(openapi_prefix="/auth")


@auth.post("/login/")
async def login(user: user):
    e = await Verify(user.email).check_regex()
    if not e:
        return JSONResponse(
            status_code=400,
            content={"status": "failed", "message": "Wrong email format!"},
        )
    check = {"email": user.email}
    if users_col.count_documents(check):
        data = users_col.find_one({"email": user.email})
        bcrypt_pass = str.encode(user.password)
        hashed = data["password"]
        if bcrypt.checkpw(bcrypt_pass, hashed):
            token = jwt.encode({"email": user.email}, jwt_secret, algorithm="HS256")
            ts = int(time.time())
            db_data = {
                "user": user.email,
                "action": "login",
                "action detail": "login successful",
                "timestamp": ts,
            }
            login_logs_col.insert_one(db_data)
            return {"status": "success", "token": token}
        else:
            ts = int(time.time())
            db_data = {
                "user": user.email,
                "action": "login",
                "action detail": "wrong password attempt",
                "timestamp": ts,
            }
            login_logs_col.insert_one(db_data)
            return JSONResponse(
                status_code=401,
                content={
                    "status": "failed",
                    "message": "Incorrect username or password!",
                },
            )
    else:
        return JSONResponse(
            status_code=401,
            content={"status": "failed", "message": "Incorrect username or password!"},
        )


@auth.post("/register/")
async def register(user: user):
    e = await Verify(user.email).check_regex()
    if not e:
        return JSONResponse(
            status_code=400,
            content={"status": "failed", "message": "Wrong email format!"},
        )
    check = {"email": user.email}
    if users_col.count_documents(check):
        return JSONResponse(
            status_code=409,
            content={"status": "failed", "message": "Email already taken!"},
        )
    else:
        bcrypt_pass = str.encode(user.password)
        hashed = bcrypt.hashpw(bcrypt_pass, bcrypt.gensalt())
        q = {"email": user.email, "password": hashed}
        x = users_col.insert_one(q)
        ts = int(time.time())
        db_data = {
            "user": user.email,
            "action": "register",
            "action detail": "register successful",
            "timestamp": ts,
        }
        login_logs_col.insert_one(db_data)
        return {"status": "success", "message": "Success!"}
