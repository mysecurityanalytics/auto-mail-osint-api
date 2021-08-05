from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import jwt, os
from modules.scan_platforms import Scan_Platforms
from modules.verify import Verify
from core.db_log import logging

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
    return response


@scan.get("/social/{email}")
def scan_social(email: str, request: Request):
    e = Verify(email).check_regex()
    if not e:
        return JSONResponse(
            status_code=400,
            content={"status": "failed", "message": "Wrong email format!"},
        )
    e = Scan_Platforms(email).scan_social()
    if e == 0:
        raise HTTPException(status_code=500, detail="System error!")
    token = request.headers["Authorization"].split(" ")[-1]
    l = logging(email).insert_db(token)
    return {"email": email, "social platforms": e}


# PoC
@scan.get("/providers/{email}")
async def scan_mailbox_providers(email: str, request: Request):
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
    token = request.headers["Authorization"].split(" ")[-1]
    l = logging(email).insert_db(token)
    return {"email": email, "mailbox provider": e}
