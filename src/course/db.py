import os
import time

import pymysql
from dotenv import load_dotenv
from loguru import logger

load_dotenv()
db = pymysql.connect(host=os.getenv("MYSQL_HOST"),
                     user=os.getenv('MYSQL_USER'),
                     password=os.getenv('MYSQL_PASSWORD'),
                     database=os.getenv('MYSQL_DATABASE'))
cursor = db.cursor()


def saveCourse(courseDataList, classList):
    # sqlStr = "truncate class_course"
    # cursor.execute(sqlStr)
    logger.info("清空数据成功")
    sqlStr = "INSERT INTO `class_course`(`className`,`week`,`weekDay`,`courseList`) VALUES(%s, %s,%s,%s)"
    start = time.perf_counter()
    try:
        cursor.executemany(sqlStr, courseDataList)
    except pymysql.Error as e:
        print(e)
        db.rollback()
        db.close()
    sqlStr = "truncate class_list"
    cursor.execute(sqlStr)
    logger.info("清空班级列表数据成功")
    sqlStr = "INSERT INTO `class_list`(`className`) VALUES(%s)"
    try:
        cursor.executemany(sqlStr, classList)
    except pymysql.Error as e:
        print(e)
        db.rollback()
        db.close()
    db.commit()
    logger.info("更新班级列表数据成功")
    end = time.perf_counter()
    logger.info("保存学生课表数据用时：%.2f秒,数据条数为:%d" % (end - start, len(courseDataList)))


def addUpdateCourseLog(author):
    currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sqlStr = f"insert into update_log(updateTime,updateAuthor) value ('{currentTime}','{author}')"
    cursor.execute(sqlStr)
    try:
        db.commit()
        logger.info("添加更新课表日志成功")
    except:
        db.rollback()
        print("添加更新课表日志失败")


def clearCourseData():
    sqlStr = "truncate table class_course"
    cursor.execute(sqlStr)
    try:
        db.commit()
        print("清空课表成功")
    except:
        db.rollback()
        print("清空课表失败")
