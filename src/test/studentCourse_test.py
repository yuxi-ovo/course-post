import logging

from bs4 import BeautifulSoup

from src.course.main import getClass

logger = logging.getLogger(__name__)


class TestStudentCourse:
    def test_classList(self):
        f = open("/Users/zhangrui/Desktop/coursePost/src/assest/教师课表_个人中心.html", 'r')
        soup = BeautifulSoup(f.read(), "html.parser")
        courseList = getClass(soup)
        assert "软件2301班" in courseList
        assert "不存在的班级" not in courseList
