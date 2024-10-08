from datetime import datetime
from fastapi import Cookie, Depends, FastAPI, HTTPException, Request, status
from fastapi_pagination import add_pagination
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated, Union
from pydantic import BaseModel

from authentication import User, UserAnonymousException, get_user, save_userdata
from game import get_players_without, get_players_for_ids

app = FastAPI()
add_pagination(app)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

from authentication import router as auth_router
app.include_router(auth_router, prefix="/auth", tags=["authentication"])

@app.get("/auth/login.html", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.get("/auth/logout.html", response_class=HTMLResponse)
async def index(request: Request):
    response = RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("jwt")
    return response


@app.exception_handler(UserAnonymousException)
async def user_anonymous_exception_handler(request: Request, exc: UserAnonymousException):
    return RedirectResponse(
        '/auth/login.html?auth=false',
        status_code=status.HTTP_302_FOUND
    )
    
@app.get("/", response_class=HTMLResponse)
async def index(request: Request, user: Annotated[str, Depends(get_user)]):
    user.players = get_players_for_ids(user.player_ids)
    context={
        "user": user,
        "players": get_players_without(user.player_ids)
    }
    return templates.TemplateResponse(request=request, name="index.html",context=context)

@app.post("/buy-player/{player_id}", response_class=HTMLResponse)
async def index(request: Request, player_id: str, user: Annotated[str, Depends(get_user)]):
    user.assets += -2 if user.assets >= 2 else 0
    user.status += 4
    user.player_ids = player_id if user.player_ids == '' else user.player_ids + ',' + player_id
    print(user.player_ids)
    context={
        "user": user
    }
    response = templates.TemplateResponse(request=request, name="stats.html",context=context)
    save_userdata(user, response)
    return response
