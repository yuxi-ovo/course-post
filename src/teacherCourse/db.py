import time
from typing import List, Tuple

import pymysql
from loguru import logger

config = {

}

# db = pymysql.connect(host='localhost', user='root', password='20050703', database='Course')
db = pymysql.connect(host="114.132.175.70", user="Course", password="NRNdLmpmWpx6jMRT", database='Course')
cursor = db.cursor()


def saveCourse(courseDataList: List[Tuple[str, str, str, str]], tech_list):
    sqlStr = "truncate tech_course"
    cursor.execute(sqlStr)
    logger.info("清空数据成功")
    sqlStr = "INSERT INTO `tech_course`(`tech_name`,`week`,`weekDay`,`courseList`) VALUES(%s, %s,%s,%s)"
    start = time.perf_counter()
    try:
        cursor.executemany(sqlStr, courseDataList)
    except pymysql.Error as e:
        print(e)
        db.rollback()
        db.close()
    sqlStr = "truncate tech_list"
    cursor.execute(sqlStr)
    logger.info("清空老师列表数据成功")
    sqlStr = "INSERT INTO `tech_list`(`tech_name`) VALUES (%s)"
    try:
        cursor.executemany(sqlStr, tech_list)
    except pymysql.Error as e:
        print(e)
        db.rollback()
        db.close()
    logger.info("老师列表数据更新成功")
    db.commit()
    db.close()
    end = time.perf_counter()
    logger.info("保存老师课表数据用时：%.2f秒,数据条数为:%d" % (end - start, len(courseDataList)))
    logger.info("老师课表更新成功")
