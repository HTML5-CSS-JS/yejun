from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# 현재 디렉터리를 템플릿 경로로 지정
templates = Jinja2Templates(directory=os.path.dirname(__file__))

# 브라우저 버전 차단 미들웨어
@app.middleware("http")
async def block_old_browsers(request: Request, call_next):
    ua = request.headers.get("user-agent", "").lower()

    # IE 차단
    if "msie" in ua or "trident" in ua:
        raise HTTPException(status_code=500)

    # Chrome 버전 확인
    if "chrome/" in ua:
        try:
            version = int(ua.split("chrome/")[1].split(" ")[0].split(".")[0])
            if version <= 67:
                raise HTTPException(status_code=500)
        except:
            pass

    # Firefox 버전 확인
    if "firefox/" in ua:
        try:
            version = int(ua.split("firefox/")[1].split(".")[0])
            if version <= 42:
                raise HTTPException(status_code=500)
        except:
            pass

    response = await call_next(request)
    return response

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("asdf.html", {"request": request, "name": "Yejun"})
