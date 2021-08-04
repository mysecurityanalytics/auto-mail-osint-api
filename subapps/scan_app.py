from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import jwt, os
from modules.scan_platforms import Scan_Platforms
from modules.verify import Verify

scan = FastAPI(openapi_prefix="/scan")

jwt_secret = os.environ.get("JWT_SECRET")


@scan.middleware("http")
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
