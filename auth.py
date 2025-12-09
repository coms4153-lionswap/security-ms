import requests
from jose import jwt
from fastapi import HTTPException
from datetime import datetime, timedelta
from database import get_connection
from sqlalchemy import text

SECRET_KEY = "LION_SWAP_GOAT_IS_THE_KEY"   
ALGO = "HS256"

def login(google_access_token: str):
    # 1. Verify google access token
    resp = requests.get(
        "https://oauth2.googleapis.com/tokeninfo",
        params={"access_token": google_access_token}
    )

    if resp.status_code != 200:
        raise HTTPException(401, "Invalid Google token")

    google_info = resp.json()
    email = google_info.get("email")

    if not email:
        raise HTTPException(400, "Google token missing email")


    query = text("""
        SELECT user_id, uni, student_name, credibility_score, avatar_url
        FROM Users
        WHERE email = :email
    """)

    with get_connection() as conn:
        user_row = conn.execute(query, {"email": email}).fetchone()

    if user_row is None:
        raise HTTPException(403, "User not found in system Users table")

    user_id, uni, student_name, cred_score, avatar = user_row

    # 3. Create your internal JWT
    now = datetime.utcnow()
    #set yuting user account to admin others are user
    role = "admin" if user_id == 1 else "user"

    payload = {
        "user_id": user_id,
        "sub": uni,                  
        "email": email,
        "name": student_name,
        "credibility": float(cred_score),
        "avatar": avatar,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=24)).timestamp())
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGO)

    return {"app_jwt": token}
