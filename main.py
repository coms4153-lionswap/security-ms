from fastapi import FastAPI
from models import LoginRequest, LoginResponse
from auth import login
from fastapi import HTTPException
from jose import jwt, JWTError
from pydantic import BaseModel

class TokenRequest(BaseModel):
    token: str
app = FastAPI(title="Security Service",
              description="Handles Google OAuth verification and generates internal JWT",
              version="1.0.0")
SECRET_KEY = "LION_SWAP_GOAT_IS_THE_KEY"
ALGO = "HS256"


@app.post("/security/login", response_model=LoginResponse)
def login_route(request: LoginRequest):
     return login(request.google_access_token)

# @app.post("/security/decode")
# def decode_token(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
#         return {
#         "user_id": payload.get("user_id"),
#         "uni" : payload.get("uni"),
#         "role": payload.get("role")
#     }
#     except JWTError:
#         raise HTTPException(401, "Invalid or expired token")

@app.post("/security/decode")
def decode_token(req: TokenRequest):
    # 2. 从模型中取出 token
    token = req.token 
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
        return {
            "user_id": payload.get("user_id"),
            "uni" : payload.get("uni"),
            "role": payload.get("role")
        }
    except JWTError:
        raise HTTPException(401, "Invalid or expired token")
