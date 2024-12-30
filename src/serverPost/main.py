from src.course.main import getTemplate, clearRedis
from src.teacherCourse.main import getTechTemplate
from src.ulits.cookie import getCookieForServer
from src.ulits.logo import showLogo


def main():
    cookie = getCookieForServer()
    showLogo('server')
    getTemplate(cookie=cookie, user='server_auto_play')
    getTechTemplate(cookie)
    clearRedis()
    showLogo('server')


if __name__ == '__main__':
    main()
