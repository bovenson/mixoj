import pymysql
from knowledge_tree.db.db_init import init_db


pymysql.install_as_MySQLdb()
init_db()
