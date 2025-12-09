import requests
from jose import jwt
from fastapi import HTTPException
from datetime import datetime, timedelta


SECRET_KEY = "LION_SWAP_GOAT_IS_THE_KEY"   
ALGO = "HS256"
IDENTITY_SERVICE_URL = "https://ms1-identity-157498364441.us-east1.run.app"  

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


    try:
        user_resp = requests.get(IDENTITY_SERVICE_URL, params={"email": email}, timeout=5)
    except Exception:
        raise HTTPException(500, "Identity service unavailable")

    if user_resp.status_code != 200:
        raise HTTPException(403, "User not found in identity service")

    user_id_str = user_resp.text.strip()

    #then i need to call sally's microserive endpoint to return the user_id, and if user_id is 7 hard_code a role to "admin and then the rest is user" 
    if not user_id_str.isdigit():
        raise HTTPException(500, f"Invalid user_id returned: {user_id_str}")

    user_id = int(user_id_str)

    role = "admin" if user_id == 7 else "user"

    now = datetime.utcnow()
    payload = {
        "user_id": user_id,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=24)).timestamp())
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGO)

    return {"app_jwt": token}
