from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import jwt
from modules.verify import Verify
import os

verify = FastAPI(openapi_prefix="/verify")

jwt_secret = os.environ.get("JWT_SECRET")


@verify.middleware("http")
async def auth_middleware(request: Request, call_next):
    response = await call_next(request)
    headers = response.headers
    if "jwt_token" in headers:
        token = response.headers["jwt_token"]
        try:
            data = jwt.decode(token, jwt_secret, algorithms=["HS256"])
            return response
        except:
            return JSONResponse(status_code=403)
    else:
        return JSONResponse(status_code=403)


@verify.get("/format/{email}")
async def check_email_regex(email: str):

    e = await Verify(email).check_regex()
    return {"email": email, "format": e}


@verify.get("/mailbox/{email}")
async def check_mailbox_exist(email: str):

    e = await Verify(email).check_mailbox()
    if e == 0:
        raise HTTPException(status_code=500, detail="System error!")
    return {"email": email, "mailbox": e}


@verify.get("/smtp/{email}")
async def check_smtp_exist(email: str):
    ports = [25, 465, 587, 2525]
    for x in range(len(ports)):
        e = await Verify(email).check_smtp(ports[x])
        if e:
            break
    return {"email": email, "smtp": e}


@verify.get("/all/{email}")
async def verify_all(email: str):

    e = Verify(email)
    return {
        "email": email,
        "format": await e.check_regex(),
        "mailbox": await e.check_mailbox(),
        "smtp": await e.check_smtp(),
    }
