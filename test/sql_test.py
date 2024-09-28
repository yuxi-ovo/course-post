import os

import pymysql

from settings import initLoadEnv

initLoadEnv()


class TestSql:
    def test_sql_localhost(self):
        host = os.getenv('MYSQL_HOST')
        user = os.getenv('MYSQL_USER')
        password = os.getenv('MYSQL_PASSWORD')
        database = os.getenv('MYSQL_DATABASE')
        assert host == '127.0.0.1'
        assert user == 'root'
        assert password == '20050703'
        assert database == 'course'
        try:
            pymysql.connect(host=host, user=user, password=password, database=database)
            assert True
        except pymysql.Error as e:
            assert False

    def test_sql_remote(self):
        host = os.getenv('REMOTE_MYSQL_HOST')
        user = os.getenv('REMOTE_MYSQL_USER')
        password = os.getenv('REMOTE_MYSQL_PASSWORD')
        database = os.getenv('REMOTE_MYSQL_DATABASE')
        assert host == '114.132.175.70'
        assert user == 'Course'
        assert password == 'NRNdLmpmWpx6jMRT'
        assert database == 'course'
        try:
            pymysql.connect(host=host, user=user, password=password, database=database)
            assert True
        except pymysql.Error as e:
            assert False
