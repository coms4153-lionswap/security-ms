from pydantic import BaseModel

class LoginRequest(BaseModel):
    google_access_token: str

class LoginResponse(BaseModel):
    app_jwt: str
