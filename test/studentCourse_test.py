import logging

from bs4 import BeautifulSoup

from src.course.main import getClass, getClassCourse

logger = logging.getLogger(__name__)

f = open("src/assest/学生课表_个人中心.html", 'r')
soup = BeautifulSoup(f.read(), "html.parser")


class TestStudentCourse:
    courseList = getClass(soup)

    def test_classList(self):
        assert "软件2301班" in self.courseList
        assert "不存在的班级" not in self.courseList

    def test_AnalyzeCourse(self):
        getClassCourse(self.courseList, soup)
        assert len(self.courseList) > 0
