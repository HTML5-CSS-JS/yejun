from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

templates = Jinja2Templates(directory=os.path.dirname(__file__))

@app.middleware("http")
async def block_old_browsers(request: Request, call_next):
    ua = request.headers.get("user-agent", "").lower()

    # IE 차단
    if "msie" in ua or "trident" in ua:
        return Response(status_code=500)

    # Chrome 버전 확인
    if "chrome/" in ua:
        try:
            version = int(ua.split("chrome/")[1].split(" ")[0].split(".")[0])
            if version <= 67:
                return Response(status_code=500)
        except:
            pass

    # Firefox 데스크톱 버전 확인 (모바일 제외)
    if "firefox/" in ua and "mobile" not in ua and "android" not in ua:
        try:
            version = int(ua.split("firefox/")[1].split(".")[0])
            if version <= 42:
                return Response(status_code=500)
        except:
            pass

    # iOS용 Firefox (FxiOS)
    if "fxios/" in ua:
        try:
            version = int(ua.split("fxios/")[1].split(".")[0])
            if version <= 42:
                return Response(status_code=500)
        except:
            pass

    response = await call_next(request)
    return response

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("asdf.html", {"request": request, "name": "Yejun"})
