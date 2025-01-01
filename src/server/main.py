from datetime import datetime

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.course.desktopCourse import getDesktopHtml
from src.score.main import getScore

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 允许的来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许的所有 HTTP 方法
    allow_headers=["*"],  # 允许的所有头
)


class Result:
    def __init__(self, data: list, code: int = 200, date=datetime.now(), msg: str = "请求成功", ):
        self.msg = msg
        self.data = data
        self.code = code
        self.date = date


@app.get("/user/score")
async def root(username: str, password: str):
    data = getScore(username, password)
    return Result(data=data)


@app.get("/user/course")
async def userCourse(username: str, password: str):
    return getDesktopHtml(username, password)
