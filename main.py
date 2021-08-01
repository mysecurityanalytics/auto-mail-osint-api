from fastapi import FastAPI
from subapps.auth_app import auth
from subapps.verify_app import verify
from subapps.scan_app import scan
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/auth", auth)
app.mount("/verify", verify)
app.mount("/scan", scan)


@app.get("/")
def root():
    return {"message": "alive"}
