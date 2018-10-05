# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 15:43:03 2016
Data Access Layer
@author: shice
"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class Oracle(object):
    """
    Oracle 连接
    """

    def __init__(self, user, pwd, ip, port, database):
        import cx_Oracle
        connstr = '{}/{}@{}:{}/{}'.format(user, pwd, ip, port, database)
        self._conn = cx_Oracle.connect(connstr)
        self._cursor = self._conn.cursor()

    def execute(self, sql):
        self._cursor.execute(sql)
        return self._cursor.rowcount, self._cursor.fetchall()

    def close(self):
        self._cursor.close
        self._conn.close()


class Mysql(object):
    """
    Mysql 连接
    """

    def __init__(self, ip, port, user, pwd, database, charset="utf8", autocommit=1):
        import MySQLdb
        connjson = {}
        connjson["host"] = ip
        connjson["port"] = int(port)
        connjson["user"] = user
        connjson["passwd"] = pwd
        connjson["db"] = database
        connjson["charset"] = "utf8"
        self._conn = MySQLdb.connect(**connjson)
        self._conn.autocommit(autocommit)
        self._cursor = self._conn.cursor()

    def execute(self, sql):
        self._cursor.execute(sql)
        return self._cursor.rowcount, self._cursor.fetchall()

    def commit(self):
        self._conn.commit()

    def close(self):
        self._cursor.close
        self._conn.close()


class SqlServel(object):
    """
    sql server 数据连接
    """
    def __init__(self, ip, port, user, pwd, database):
        import pyodbc

        # CHARSET=UTF8;TDS_Version=8.0;
        # if mode == 0:
        #     connstr = 'DRIVER=FreeTDS;SERVER={};port={};DATABASE={};UID={};PWD={};'.format(ip, port, database, user,
        #                                                                                    pwd)
        # else:
        connstr = 'DRIVER=FreeTDS;SERVER={};port={};DATABASE={};UID={};PWD={};CHARSET=UTF8;TDS_Version=8.0;'.format(
                ip, port, database, user, pwd)

        self._conn = pyodbc.connect(connstr)
        self._cursor = self._conn.cursor()

    def execute(self, sql):
        self._cursor.execute(sql)
        return self._cursor.rowcount, self._cursor.fetchall()

#    def insert(self, sql):
#        self._cursor.execute(sql)
#        self._conn.commit()
#        return self._cursor.rowcount

    def close(self):
        self._cursor.close()
        self._conn.close()
