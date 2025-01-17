import time
from datetime import datetime
from functools import wraps

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.score.main import getScore, getUnCourse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 允许的来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许的所有 HTTP 方法
    allow_headers=["*"],  # 允许的所有头
)


class Result:
    def __init__(self, data: list, code: int = 200, currentTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                 msg: str = "请求成功", ):
        self.msg = msg
        self.data = data
        self.code = code
        self.currentTime = currentTime


def print_runtime(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        runtime = end_time - start_time
        print(f"Function '{func.__name__}' executed in {runtime:.4f} seconds")
        return result

    return wrapper


@print_runtime
@app.get("/user/score")
async def root(username: str, password: str):
    data = getScore(username, password)
    return Result(data=data)


@app.get("/user/unCourse")
async def root(username: str, password: str):
    data = getUnCourse(username, password)
    return Result(data=data)

# @app.get("/user/course")
# async def userCourse(username: str, password: str):
#     return getDesktopHtml(username, password)
