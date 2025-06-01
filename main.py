from fastapi import FastAPI
from fastapi import Request                    # テンプレートにリクエストを渡すために必要
from fastapi import Form                       # フォームあら値を受け取るために必要
from fastapi.responses import HTMLResponse     # htmlレスポンスを返すために必要
from fastapi.responses import RedirectResponse # リダイレクトレスポンスを返すために必要
from fastapi.templating import Jinja2Templates # Jinja2テンプレートを使用するために必要
from starlette.middleware.sessions import SessionMiddleware  # セッションミドルウェアを使用するために必要

app = FastAPI()
# セッションを使用するためのミドルウェアを追加
app.add_middleware(SessionMiddleware, secret_key="session_key")  
# 指定したディレクトリをjinja2のテンプレートディレクトリとして設定
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # index.htmlをtemplatesから探し、messageに値を渡してレンダリングする
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submit")
# formのname=nameからstring型の値を受け取る
async def submit(request: Request, name: str = Form()):
    # セッションに値を保存
    request.session["name"] = name
    # フォームから受け取った値をクエリに乗せてリダイレクト
    return RedirectResponse(url="/result", status_code=302)

@app.get("/result", response_class=HTMLResponse)
async def result(request: Request):
    # セッションから値を取得
    name = request.session.get("name", "FastAPI")
    return templates.TemplateResponse("result.html", {"request": request, "name": name})