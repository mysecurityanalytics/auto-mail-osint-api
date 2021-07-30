from fastapi import FastAPI
from subapps.verify_app import verify
from subapps.auth_app import auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/verify", verify)
app.mount("/auth", auth)


@app.get("/")
def root():
    return {"message": "alive"}
