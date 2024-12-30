import json
import urllib.request

from bs4 import BeautifulSoup
from loguru import logger

from src.teacherCourse.db import saveCourse

a = {
    "老师名": {
        "第几周": {
            "星期几": {
                "第几节": {
                    "课程信息": {

                    }
                }
            }
        }
    }
}


def getCookie():
    import time

    from selenium import webdriver
    from selenium.webdriver.common.by import By

    # 启动浏览器
    driver = webdriver.Firefox()  # 如果你使用的是Firefox浏览器

    # 打开登录页面
    driver.get(
        "https://authserver.hniu.cn/authserver/login?service=https%3A%2F%2Fehall.hniu.cn%3A443%2Flogin%3Fservice%3Dhttps%3A%2F%2Fehall.hniu.cn%2Fnew%2Findex.html%3Fbrowser%3Dno")

    # 找到用户名输入框并输入账户
    username_input = driver.find_element(By.ID, 'username')
    username_input.send_keys("202315310305")

    # 找到密码输入框并输入密码
    password_input = driver.find_element(By.ID, 'password')
    password_input.send_keys("20050703zrZR")

    # 找到登录按钮并点击
    login_button = driver.find_element(By.CLASS_NAME, 'auth_login_btn')
    login_button.click()

    system_button = driver.find_element(By.CLASS_NAME, "widget-title")
    system_button.click()

    going_button = driver.find_element(By.ID, "ampDetailEnter")
    going_button.click()

    # 获取登录后的cookie
    # time.sleep(10)
    time.sleep(3)
    search_window = driver.window_handles
    driver.switch_to.window(search_window[1])
    # week = driver.find_element(By.CLASS_NAME, "layui-tab-content")
    # week.click()
    cookies = driver.get_cookies()
    cookie = ""
    for c in cookies:
        if c.get('name') == "bzb_jsxsd":
            cookie = c.get('value')
    driver.quit()
    return cookie


def getTechTemplate(cookie):
    url = 'https://jw.hniu.cn/jsxsd/kbcx/kbxx_teacher_ifr';
    head = {
        "cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15"
    }
    data = urllib.parse.urlencode({"xnxqh": "2024-2025-1", "kbjcmsid": "67FB3A89FDC146ADA865DCC81B9EC143"}).encode(
        "utf-8")
    request = urllib.request.Request(url, headers=head, method="POST", data=data)
    response = urllib.request.urlopen(request)
    html = response.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")
    teacherCourseList = getTechNameLst(soup)

    # print(name)
    getTeacherCourse(soup, teacherCourseList)
    logger.info("爬取老师课表数据成功")
    courseDataList = []
    tech_list = []
    for tName in teacherCourseList:
        tech_list.append((tName,))
        for week in teacherCourseList[tName]:
            # print("周次", week)
            for weekDay in teacherCourseList[tName][week]:
                # print("星期几", weekDay)
                # print("这天的课:", teacherCourseList[tName][week][weekDay])
                # saveCourse(tName, week, weekDay, teacherCourseList[tName][week][weekDay])
                courseData = teacherCourseList[tName][week][weekDay]
                courseData = json.dumps(courseData, ensure_ascii=False)
                courseDataList.append((tName, week, weekDay, courseData))
    saveCourse(courseDataList, tech_list)
    logger.info("保存老师课表数据成功!")


def getTechNameLst(soup):
    techNameList = []
    r = {}
    rowList = soup.find("table").findChildren("tr")[2:]
    liuTingIndex = 0
    for d in rowList:
        tech_name = d.find("td").text.strip()
        if tech_name == '刘婷':
            liuTingIndex += 1
            tech_name = '刘婷' + str(liuTingIndex)
            techNameList.append(tech_name)
        else:
            techNameList.append(tech_name)
    for name in techNameList:
        r[name] = {}
    return r


def getTeacherCourse(soup, teacherCourseList):
    rowList = soup.find("table").findChildren("tr")[2:]
    section = ["第一大节", "第二大节", "第三大节", "第四大节", "第五大节", "第六大节"]
    weekDay = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekDayIndex = 0
    sectionIndex = 0
    liuTingIndex = 0
    for row in rowList:
        weekDayIndex = 0
        sectionIndex = 0
        if row.text == '\n':
            continue
        contentList = row.findChildren("nobr")
        for content in contentList:
            # 没课
            if len(content.text.strip()) == 0:
                sectionIndex += 1
                if sectionIndex > 5:
                    weekDayIndex += 1
                    sectionIndex = 0
                if weekDayIndex > 6:
                    weekDayIndex = 0
                    sectionIndex = 0
                continue
            # 老师名字
            elif len(content.text.strip()) <= 6:
                # 名字
                if content.text.strip() == '刘婷':
                    liuTingIndex += 1
                continue
            # 正常处理课程逻辑
            for k in content.contents:
                if k == '\n':
                    continue
                # print("k", k)
                courseList = str(k).split("<br/>")
                courseData = {}
                # print("courseList", courseList)
                courseName = courseList[0][30:]
                courseClass = courseList[1]
                courseTeacher = courseList[2].split('\n')[1].strip()
                courseWeek = courseList[2].split('\n')[2].strip()
                coursePosition = courseList[3].split('\n')[1].strip()
                courseSection = section[sectionIndex]
                courseWeekDay = weekDay[weekDayIndex]

                courseData["courseTeacher"] = courseTeacher
                courseData["courseName"] = courseName
                courseData["courseClass"] = courseClass
                courseData["courseWeek"] = courseWeek
                courseData["coursePosition"] = coursePosition
                courseData["courseSection"] = courseSection
                courseData["courseWeekDay"] = courseWeekDay
                # print("courseData", courseData)
                # print(courseName)
                if courseTeacher == '刘婷':
                    courseData["courseTeacher"] = "刘婷" + str(liuTingIndex)

                addWeekCourse(teacherCourseList, courseData["courseTeacher"], weekDay[weekDayIndex],
                              section[sectionIndex],
                              courseData)
            sectionIndex += 1
            if sectionIndex > 5:
                weekDayIndex += 1
                sectionIndex = 0
            if weekDayIndex > 6:
                weekDayIndex = 0
                sectionIndex = 0

    return teacherCourseList


def addWeekCourse(courseList, teacherName, weekDay, section, courseData):
    courseData['courseWeek'] = courseData.get('courseWeek').replace("(", "").replace(")", "")
    weekData = courseData.get('courseWeek').split(",")

    if len(weekData) != 1:
        for i in weekData:
            temp = i.split("-")
            if len(temp) != 1:
                # print("连续的", temp)
                minWeek = temp[0].replace("周", "")
                maxWeek = temp[1].replace("周", "")
                addCourse(maxWeek, minWeek, courseList, teacherName, weekDay, section, courseData)
            else:
                # print("单周", temp)
                if '单' in temp[0]:
                    maxWeek = 0
                    minWeek = temp[0][0]
                    print(minWeek)
                    addCourse(maxWeek, minWeek, courseList, teacherName, weekDay, section, courseData)
                    continue
                addCourse(0, temp[0].replace("周", ""), courseList, teacherName, weekDay, section, courseData)

    else:
        for i in weekData:
            temp = i.split("-")
            if len(temp) != 1:
                # print("单周连续的", temp)
                minWeek = temp[0].replace("周", "")
                maxWeek = temp[1].replace("周", "")
                addCourse(maxWeek, minWeek, courseList, teacherName, weekDay, section, courseData)
            else:
                # print("单独单周", temp)
                if '单' in temp[0]:
                    maxWeek = 0
                    minWeek = temp[0][0]
                    addCourse(maxWeek, minWeek, courseList, teacherName, weekDay, section, courseData)
                    continue
                addCourse(0, temp[0].replace("周", ""), courseList, teacherName, weekDay, section, courseData)


def addCourse(maxWeek, minWeek, courseList, teacherName, weekDay, section, courseData):
    maxWeek = int(maxWeek)
    minWeek = int(minWeek)

    def add():
        if week not in courseList[teacherName]:
            courseList[teacherName][week] = {}
        if weekDay not in courseList[teacherName][week]:
            courseList[teacherName][week][weekDay] = {}
        if section not in courseList[teacherName][week][weekDay]:
            courseList[teacherName][week][weekDay][section] = {}
        courseList[teacherName][week][weekDay][section] = courseData

    if maxWeek == 0:
        week = "第{}周".format(minWeek)
        add()
        return
    for i in range(minWeek, maxWeek + 1):
        week = "第{}周".format(i)
        add()
