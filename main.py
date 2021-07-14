from fastapi import FastAPI
import pymongo
from modules.verify import Verify

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/verify/format/{email}")
async def check_email_regex(email: str):

    e = await Verify(email).check_regex()
    return {"email": email, "format": e}


@app.get("/verify/mailbox/{email}")
async def check_mailbox_exist(email: str):

    e = await Verify(email).check_mailbox()
    return {"email": email, "mailbox": e}


@app.get("/verify/smtp/{email}")
async def check_smtp_exist(email: str):

    e = await Verify(email).check_smtp()
    return {"email": email, "smtp": e}


@app.get("/verify/all/{email}")
async def verify_all(email: str):

    e = Verify(email)
    return {"email": email, "format": await e.check_regex(), "mailbox": await e.check_mailbox(), "smtp": await e.check_smtp()}
