from datetime import datetime, timedelta
from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError, PyJWKError
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status, Request
from fastapi.responses import Response, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
TOKEN_SECRET_KEY = "72c14e6b0ac97a6fe571cda98172f09e0bf630414677cb3a6456201544eb9b81"
TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def create_jw_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

router = APIRouter()

class User():
    def __init__(self, username: str, assets: int | None = 100, status: int | None = 0, potential: int | None = 0):
        self.username = username
        self.assets = assets
        self.status = status
        self.potential = potential
        self.player_ids = ''
        
@router.post("/token")
async def login_for_jwt(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    response = RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)
    save_userdata(User(form_data.username), response)
    return response

def decode_token(token: str, key: str | None = None) -> str | None:
    try:
        payload = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        if key:
            return payload.get(key)
        return payload.get('sub')
    except PyJWKError as e:
        print(e)
        return None
    
class Cookies(BaseModel):
    access_token: str
    refresh_token: str

def check_cookie(request: Request):
    cookie = request.cookies
    if not cookie:
        return None
    if cookie.get('jwt'):
        return cookie.get('jwt')
    
class UserAnonymousException(Exception):
    def __init__(self, message: str):
        self.message = message
        
def get_user(request: Request) -> User | None:
    token = check_cookie(request)
    if token != None:
        username = decode_token(token, 'sub')
        expires = decode_token(token, 'exp')
        print(f"expires: {datetime.fromtimestamp(expires)}")
        assets = decode_token(token, 'assets')
        status = decode_token(token, 'status')
        potential = decode_token(token, 'status')
        user = User(username, assets, status, potential)
        user.player_ids = decode_token(token, 'player_ids')
        return user
    raise UserAnonymousException(message="user not authenticated")

def save_userdata(user: User, response: Response):
    jw_token = create_jw_token(data={
        "sub": user.username,
        "assets": user.assets,
        "status": user.status,
        "potential": user.potential,
        "player_ids": user.player_ids
    })
    response.set_cookie(key="jwt", value=jw_token, httponly=True)
    