from src.course.main import getCookie, getTemplate, clearRedis
from src.teacherCourse.main import getTechTemplate

if __name__ == '__main__':
    cookie = getCookie()
    # cookie = ''
    getTemplate(cookie)
    getTechTemplate(cookie)
    clearRedis()
