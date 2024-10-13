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
from players import Players, Player

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
    
UserDep = Annotated[str, Depends(get_user)]

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, user: UserDep):
    return templates.TemplateResponse(request=request, name="index.html",context={"user": user})

PlayersDep = Annotated[Players, Depends(Players)]

@app.get("/board.html", response_class=HTMLResponse)
async def board(request: Request, user: UserDep, players: PlayersDep):
    user.players = players.get_players_for_ids(user.player_ids)
    context={
        "user": user,
        "players": players.get_players_without(user.player_ids)
    }
    return templates.TemplateResponse(request=request, name="update_board.html",context=context)

@app.post("/select-player/{player_id}", response_class=HTMLResponse)
async def select_player_in_draft(request: Request, player_id: str, user: UserDep, players: PlayersDep):
    player = players.get_player_by_id(player_id)
    user.status += player.status
    user.player_ids = player_id if user.player_ids == '' else user.player_ids + ',' + player_id
    user.players = players.get_players_for_ids(user.player_ids)
    context={
        "user": user,
        "players": players.get_players_without(user.player_ids)
    }
    response = templates.TemplateResponse(request=request, name="update_board.html",context=context)
    save_userdata(user, response)
    return response

@app.post("/deselect-player/{player_id}", response_class=HTMLResponse)
async def deselect_player(request: Request, player_id: str, user: UserDep, players: PlayersDep):
    print(player_id)
    player = players.get_player_by_id(player_id)
    user.status -= player.status
    a = user.player_ids.split(',')
    a.remove(player_id)
    user.player_ids = ",".join(a)
    user.players = players.get_players_for_ids(user.player_ids)
    context={
        "user": user,
        "players": players.get_players_without(user.player_ids)
    }
    response = templates.TemplateResponse(request=request, name="update_board.html",context=context)
    save_userdata(user, response)
    return response


@app.post("/buy-player/{player_id}", response_class=HTMLResponse)
async def buy_player(request: Request, player_id: str, user: UserDep, players: PlayersDep):
    player = players.get_player_by_id(player_id)
    if user.assets - player.price > 0:
        user.assets += -1 * player.price
        user.status += player.status
        user.player_ids = player_id if user.player_ids == '' else user.player_ids + ',' + player_id
    user.players = players.get_players_for_ids(user.player_ids)
    context={
        "user": user,
        "players": players.get_players_without(user.player_ids)
    }
    response = templates.TemplateResponse(request=request, name="update_board.html",context=context)
    save_userdata(user, response)
    return response

@app.post("/sell-player/{player_id}", response_class=HTMLResponse)
async def sell_player(request: Request, player_id: str, user: UserDep, players: PlayersDep):
    player = players.get_player_by_id(player_id)
    user.assets += player.scouting_price
    user.status -= player.status
    a = user.player_ids.split(',')
    a.remove(player_id)
    user.player_ids = ",".join(a)
    user.players = players.get_players_for_ids(user.player_ids)
    context={
        "user": user,
        "players": players.get_players_without(user.player_ids)
    }
    response = templates.TemplateResponse(request=request, name="update_board.html",context=context)
    save_userdata(user, response)
    return response

@app.get("/chmod", response_class=HTMLResponse)
async def sell_player(request: Request, user: UserDep, players: PlayersDep):
    user.usergroup = 'admin' if user.usergroup == 'gamer' else 'gamer'
    response = RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)
    save_userdata(user, response)
    return response

@app.get("/players.html", response_class=HTMLResponse)
async def sell_player(request: Request, user: UserDep, players: PlayersDep):
    context={
        "user": user
    }
    return templates.TemplateResponse(request=request, name="players.html",context=context)

@app.get("/players-list.html", response_class=HTMLResponse)
async def sell_player(request: Request, user: UserDep, players: PlayersDep, page: int | None = 1, size: int | None = 16):
    context={
        "user": user,
        "players": players.get_players('/players-list.html', page, size)
    }
    return templates.TemplateResponse(request=request, name="players_list.html",context=context)