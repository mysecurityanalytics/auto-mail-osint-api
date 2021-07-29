from fastapi import FastAPI
from subapps.verify_app import verify
from subapps.auth_app import auth

app = FastAPI()

app.mount("/verify", verify)
app.mount("/auth", auth)


@app.get("/")
def root():
    return {"message": "alive"}
