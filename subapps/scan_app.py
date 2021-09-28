from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import jwt, os
from modules.scan_platforms import Scan_Platforms
from modules.verify import Verify
import pymongo
import time
import re

db_url = os.environ.get("MONGO_URI")
client = pymongo.MongoClient(db_url)
db = os.environ.get("DB_NAME")
logs_col = client[db]["logs"]

scan = FastAPI(openapi_prefix="/scan")

jwt_secret = os.environ.get("JWT_SECRET")


@scan.middleware("http")
async def auth_middleware(request: Request, call_next):
    headers = request.headers
    if "Authorization" in headers:
        token = request.headers["Authorization"].split(" ")[-1]
        print(token)
        try:
            data = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        except:
            return JSONResponse(status_code=403)
    else:
        return JSONResponse(status_code=403)

    response = await call_next(request)
    user = str(data["email"])
    url = str(request.url)
    checked_email = re.findall("([^\/]+$)", url)
    ts = int(time.time())
    db_data = {"user": user, "checked_email": str(checked_email[0]), "timestamp": ts}
    logs_col.insert_one(db_data)
    return response


@scan.get("/social/{email}")
def scan_social(email: str):
    e = Verify(email).check_regex()
    if not e:
        return JSONResponse(
            status_code=400,
            content={"status": "failed", "message": "Wrong email format!"},
        )
    e = Scan_Platforms(email).scan_social()
    if e == 0:
        raise HTTPException(status_code=500, detail="System error!")
    return {"email": email, "social platforms": e}


# PoC
@scan.get("/providers/{email}")
async def scan_mailbox_providers(email: str):
    e = await Verify(email).check_regex()
    if not e:
        return JSONResponse(
            status_code=400,
            content={"status": "failed", "message": "Wrong email format!"},
        )
    e = await Scan_Platforms(email).scan_mailbox_providers()
    if e == 0:
        raise HTTPException(status_code=500, detail="System error!")
    if e == None:
        raise HTTPException(status_code=404, detail="Domain not found!")
    return {"email": email, "mailbox provider": e}
