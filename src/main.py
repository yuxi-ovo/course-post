import pyfiglet

from src.course.main import clearRedis, getCookie, getTemplate
from src.teacherCourse.main import getTechTemplate


def showLogo():
    figlet_text = pyfiglet.Figlet(font='Soft')
    color_text = figlet_text.renderText('coursePost')
    print(color_text)


if __name__ == '__main__':
    showLogo()
    cookie = getCookie()
    getTemplate(cookie)
    getTechTemplate(cookie)
    clearRedis()
    showLogo()
