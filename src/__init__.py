import argparse

from loguru import logger

from src.course.main import clearRedis, getTemplate
from src.serverPost.main import main as serverPost
from src.teacherCourse.main import getTechTemplate
from src.ulits.cookie import getCookie
from src.ulits.logo import showLogo


def main():
    showLogo()
    cookie = getCookie()
    getTemplate(cookie)
    getTechTemplate(cookie)
    clearRedis()
    showLogo()


def run():
    # 创建解析器
    parser = argparse.ArgumentParser(description="这是一个简单的命令行工具")
    parser.add_argument("-server", action="store_true")
    parser.add_argument("-local", action="store_true")
    args = parser.parse_args()
    if args.server:
        logger.info("开始服务器端课程爬取")
        serverPost()
    else:
        logger.info("开始本地端课程爬取")
        main()


if __name__ == '__main__':
    run()
