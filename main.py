# coding: utf-8

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

templates = Jinja2Templates(directory=os.path.dirname(__file__))

@app.middleware("http")
async def block_ie(request: Request, call_next):
    ua = request.headers.get("user-agent", "").lower()

    # IE 차단 → 커스텀 메시지 반환
    if "msie" in ua or "trident" in ua:
        return HTMLResponse(
            content="<h1>error 500</h1><br><h3>야이 씨발놈아 IE를 왜씀</h3>",
            status_code=500
        )

    response = await call_next(request)
    return response

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("asdf.html", {"request": request, "name": "Yejun"})
