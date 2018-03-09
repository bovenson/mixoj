# codding: utf-8
import pymysql
from knowledge_tree.db.static_vars import *


class CommonDB(object):
    def __init__(self):
        self.res = None
        self.cursor = None
        self.conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME, charset="utf8")
        pass

    def execute(self, sql, params=()):
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
            pass
        self.cursor = self.conn.cursor()
        return self.cursor.execute(sql, params)
        pass

    def commit(self):
        self.conn.commit()
        pass

    def fetchone(self):
        _res = None
        if self.cursor is None:
            return _res
        _res = self.cursor.fetchone()
        return _res

    def fetchall(self):
        _res = None
        if self.cursor is None:
            return _res
        _res = self.cursor.fetchall()
        return _res
        pass

    def fetchmany(self, size):
        _res = None
        if self.cursor is None or size is None:
            return _res
        res = self.cursor.fetchmany(size=size)
        return _res
        pass

    def close(self):
        if self.conn is not None:
            self.conn.close()
        if self.cursor is not None:
            self.cursor.close()
    pass


if __name__ == "__main__":
    pass
