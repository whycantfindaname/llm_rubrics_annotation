# app/routes.py

from fastapi.responses import HTMLResponse
from fastapi import Request, APIRouter
from starlette.responses import RedirectResponse

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
def login_form():
    with open("app/static/login.html", "r") as f:
        return HTMLResponse(content=f.read())

@router.post("/login", response_class=HTMLResponse)
async def login_submit(request: Request):
    form_data = await request.form()
    # TODO: add authentication logic, redirect to GET /login on failure
    return RedirectResponse("/dashboard", status_code=303)

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    with open("app/static/dashboard.html", "r") as f:
        return HTMLResponse(content=f.read())
