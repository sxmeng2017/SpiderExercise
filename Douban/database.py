import pymysql
import pprint

MYSQL_DB = 'douban'
MYSQL_USER = 'root'
MYSQL_PASS = '123456'
MYSQL_HOST = '127.0.0.1'

connection = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER,
                             password=MYSQL_PASS, db=MYSQL_DB,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()

sql = 'SELECT id,url FROM start'
cursor.execute(sql)
start_datas = cursor.fetchall()

for item in start_datas:
    print(item['url'])
