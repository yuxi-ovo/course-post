from bs4 import BeautifulSoup

from src.teacherCourse.main import getTechNameLst, getTeacherCourse

f = open("src/assest/教师课表_个人中心.html", 'r')
soup = BeautifulSoup(f.read(), "html.parser")


class TestTechCourse:
    techNamelist = getTechNameLst(soup)

    def test_classList(self):
        assert "严双" in self.techNamelist
        assert "不存在的老师" not in self.techNamelist

    def test_AnalyzeCourse(self):
        getTeacherCourse(soup, self.techNamelist)
        assert len(self.techNamelist) > 0
