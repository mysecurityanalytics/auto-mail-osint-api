from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import jwt
from modules.verify import Verify
import os
from core.db_log import logging

verify = FastAPI(openapi_prefix="/verify")

jwt_secret = os.environ.get("JWT_SECRET")


@verify.middleware("http")
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


@verify.get("/format/{email}")
async def check_email_regex(email: str, request: Request):

    e = await Verify(email).check_regex()
    token = request.headers["Authorization"].split(" ")[-1]
    l = logging(email).insert_db(token)
    return {"email": email, "format": e}


@verify.get("/mailbox/{email}")
async def check_mailbox_exist(email: str, request: Request):

    e = await Verify(email).check_mailbox()
    if e == 0:
        raise HTTPException(status_code=500, detail="System error!")
    token = request.headers["Authorization"].split(" ")[-1]
    l = logging(email).insert_db(token)
    return {"email": email, "mailbox": e}


@verify.get("/smtp/{email}")
async def check_smtp_exist(email: str, request: Request):
    ports = [25, 465, 587, 2525]
    for x in range(len(ports)):
        e = await Verify(email).check_smtp(ports[x])
        if e:
            break
    token = request.headers["Authorization"].split(" ")[-1]
    l = logging(email).insert_db(token)
    return {"email": email, "smtp": e}


@verify.get("/all/{email}")
async def verify_all(email: str, request: Request):
    e = Verify(email)
    ports = [25, 465, 587, 2525]
    for x in range(len(ports)):
        is_smtp_open = await Verify(email).check_smtp(ports[x])
        if is_smtp_open:
            break
    token = request.headers["Authorization"].split(" ")[-1]
    l = logging(email).insert_db(token)
    return {
        "email": email,
        "format": await e.check_regex(),
        "mailbox": await e.check_mailbox(),
        "smtp": is_smtp_open,
    }
