# codding: utf-8
from knowledge_tree.db.common_db import CommonDB

DB_TABLE_NAME = "knowledge_tree"


def init_db():
    _db = CommonDB()

    # 没有数据表, 则新建
    sql = "SHOW TABLES"
    _db.execute(sql)
    flag = False
    for _item in _db.fetchall():
        if _item is not None and isinstance(_item, tuple):
            for _i in _item:
                if _i == DB_TABLE_NAME:
                    flag = True
                pass
        pass
    # 如果没有数据表, 新建表
    if not flag:
        # id:自增字段
        # pid: 父节点id
        # name: 节点名称
        # synonym: 节点名称同义词, 空格或者英文逗号分割
        sql = "CREATE TABLE " + DB_TABLE_NAME + "(id INT NOT NULL AUTO_INCREMENT, pid INT NOT NULL, " \
                                                "name VARCHAR(20), synonym VARCHAR(100), PRIMARY KEY(id, pid))"
        try:
            _db.execute(sql)
        except Exception as e:
            print("初始化数据库时出错: ", e)
            raise Exception("初始化数据库时出错: " + str(e))

    # 关闭数据库连接
    _db.close()
    pass


# 删除所有数据, 重新建立数据表
def rebuild_db():
    _db = CommonDB()
    # 没有数据表, 则新建
    sql = "SHOW TABLES"
    _db.execute(sql)
    flag = False
    for _item in _db.fetchall():
        if _item is not None and isinstance(_item, tuple):
            for _i in _item:
                if _i == DB_TABLE_NAME:
                    flag = True
                pass
        pass
    # 如果有数据表, 删除
    if flag:
        sql = "DROP TABLE %s" % DB_TABLE_NAME
        try:
            _db.execute(sql)
        except Exception as e:
            print("重建数据库时出错: ", e)
            raise Exception("初始化数据库时出错: " + str(e))

    # 关闭数据库连接
    _db.close()
    init_db()
    pass


if __name__ == "__main__":
    rebuild_db()
    pass
