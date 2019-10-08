import pymysql

from Douban.items import CommMeta, StartMeta


class DouBanPipeline(object):

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.client = pymysql.connect(host='127.0.0.1',
                                      user=self.user,
                                      password=self.password,
                                      db='douban',
                                      charset='utf8mb4',
                                      cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.client.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASS'),
        )

    def open_sipder(self, spider):
        print('open')

    def close_spider(self, spider):
        self.client.close()

    def get_comment(self, item):
        sql = 'SELECT * FROM new_table WHERE name=("{0}") and movie_name=("{1}")'.format(item['name'], item['movie_name'])
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def save_comment(self, item):
        keys = item.keys()
        values = tuple(item.values())
        fields = ','.join(keys)
        temp = ','.join(['%s'] * len(keys))
        sql = 'INSERT INTO new_table ({}) VALUES ({})'.format(fields, temp)
        self.cursor.execute(sql, values)
        return self.client.commit()

    def get_start(self, item):
        sql = 'SELECT * FROM start WHERE id={}'.format(item['id'])
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def save_start(self, item):
        keys = item.keys()
        values = tuple(item.values())
        fields = ','.join(keys)
        temp = ','.join(['%s'] * len(keys))
        sql = 'INSERT INTO start ({}) VALUES ({})'.format(fields, temp)
        self.cursor.execute(sql, values)
        return self.client.commit()

    def process_item(self, item, spider):
        if isinstance(item, CommMeta):
            exist = self.get_comment(item)
            if not exist:
                self.save_comment(item)

        if isinstance(item, StartMeta):
            exist = self.get_start(item)
            if not exist:
                self.save_start(item)

        return item


