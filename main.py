from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# 현재 디렉터리를 템플릿 경로로 지정
templates = Jinja2Templates(directory=os.path.dirname(__file__))

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("asdf.html", {"request": request, "name": "Yejun"})
