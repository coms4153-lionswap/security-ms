from fastapi import FastAPI
from models import LoginRequest, LoginResponse
from auth import login

app = FastAPI(title="Security Service",
              description="Handles Google OAuth verification and generates internal JWT",
              version="1.0.0")


@app.post("/security/login", response_model=LoginResponse)
def login_route(request: LoginRequest):
    return login(request.google_access_token)
