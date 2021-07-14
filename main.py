from fastapi import FastAPI
import pymongo
from verify import Verify

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/verify/format/{email}")
async def verify_format(email: str):

    e = await Verify(email).format_check()
    return {"email": email, "format": e}


@app.get("/verify/mailbox/{email}")
async def verify_mailbox(email: str):

    e = await Verify(email).mailbox_check()
    return {"email": email, "mailbox": e}


@app.get("/verify/smtp/{email}")
async def verify_smtp(email: str):

    e = await Verify(email).smtp_check()
    return {"email": email, "smtp": e}


@app.get("/verify/all/{email}")
async def verify_all(email: str):

    e = await Verify(email)
    return {"email": email, "format": e.format_check(), "mailbox": e.mailbox_check(), "smtp": e.smtp_check()}
