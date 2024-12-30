import argparse

from loguru import logger

from src import showLogo, getCookie, getTemplate, getTechTemplate, clearRedis
from src.serverPost.main import main as serverPost


def main():
    showLogo()
    cookie = getCookie()
    getTemplate(cookie)
    getTechTemplate(cookie)
    clearRedis()
    showLogo()


def run():
    # 创建解析器
    parser = argparse.ArgumentParser(description="coursePost command")
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
    # print(os.getenv("MYSQL_HOST"))
