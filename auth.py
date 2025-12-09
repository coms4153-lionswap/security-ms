import requests
from jose import jwt
from fastapi import HTTPException
from datetime import datetime, timedelta


SECRET_KEY = "LION_SWAP_GOAT_IS_THE_KEY"   
ALGO = "HS256"
IDENTITY_SERVICE_URL = "https://ms1-identity-157498364441.us-east1.run.app/users/by-email"  

def login(google_access_token: str):
    # 1. Verify google access token
    resp = requests.get(
        "https://oauth2.googleapis.com/tokeninfo",
        params={"access_token": google_access_token}
    )

    if resp.status_code != 200:
        raise HTTPException(401, "Invalid Google token")
    #decode the google token into email
    google_info = resp.json()
    email = google_info.get("email")

    if not email:
        raise HTTPException(400, "Google token missing email")

    final_url = f"{IDENTITY_SERVICE_URL}/{email}"

    try:
        user_resp = requests.get(final_url, timeout=5)
    except Exception:
        raise HTTPException(500, "Identity service unavailable")

    if user_resp.status_code != 200:
        raise HTTPException(403, "User not found in identity service")
    try:
        user_data = user_resp.json()
        user_id = int(user_data["user_id"])
    except Exception:
        raise HTTPException(500, f"Invalid response from identity service: {user_resp.text}")
    
    role = "admin" if user_id == 11 else "user"

    now = datetime.utcnow()
    payload = {
        "user_id": user_id,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=24)).timestamp()),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGO)

    return {"app_jwt": token}
