from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

USERS = {
    "user1": "pass1",
    "user2": "pass2"
}

@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if USERS.get(username) == password:
        return templates.TemplateResponse("chat.html", {"request": request, "user": username})
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})