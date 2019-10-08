
import sys
sys.path.append("..")

from Douban import database as db
from Douban.items import StartMeta

from scrapy import Request, Spider

cursor = db.connection.cursor()


class MovieStartSpider(Spider):
    name = 'movie_start'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/']

    def start_requests(self):
        headers = {
            'Referer': 'https://movie.douban.com/top250',
            'Host': 'movie.douban.com',
            'Upgrade-Insecure-Requests':1,
            'User-Agent':'Mozilla/5.0 (Macintosh;'
                         ' Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        }
        # bid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(11))
        cookies = {'Cookie':'gr_user_id=e41d54bb-8fe4-4b6a-93ba-3e995d7fcc8e;' \
                  ' _vwo_uuid_v2=D3AF0E6F140A2A6FDD6E8577FAD7C932A|f4d8ec37aa53f6af6f6a44c147094eb0;' \
                  ' douban-fav-remind=1;' \
                  ' viewed="1136881_26274202_4820710";' \
                  ' bid=jI4TcP7uMQk; trc_cookie_storage=taboola%2520global%253Auser-id%3D9b3e307e-3d91-40c2-8b80-c79c7a2aed3f-tuct29e5c04; ll="108288";' \
                  ' __yadk_uid=v9r9hokrGRQZn80YzabJbHEAe331fxeG; ps=y;' \
                  ' push_noty_num=0; push_doumail_num=0; __utmv=30149280.17538;' \
                  ' __utmc=30149280; __utmc=223695111;' \
                  ' __utmz=30149280.1570452675.37.34.utmcsr=baidu|utmccn=(organic)|utmcmd=organic;' \
                  ' __utmz=223695111.1570452675.6.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic;' \
                  ' ap_v=0,6.0;' \
                  ' _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1570458235%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DBh4Xwgh9E_aqHC_NOs0H7DpcGldaEhs2w6Kv0QoZALS30CLCuYjv6jrAjHfLHviD%26wd%3D%26eqid%3Df08b3b5200455fa3000000035d9b34be%22%5D;' \
                  ' _pk_id.100001.4cf6=e288a8d04c2cfea7.1566385347.5.1570458235.1570453885.;' \
                  ' _pk_ses.100001.4cf6=*; __utma=30149280.1038943563.1519695382.1570452675.1570458235.38;' \
                  ' __utmb=30149280.0.10.1570458235;' \
                  ' __utma=223695111.570726038.1566385347.1570452675.1570458235.7;' \
                  ' __utmb=223695111.0.10.1570458235'}
        yield Request(self.start_urls[0], headers=headers, cookies=cookies)


    def parse(self, response):
        for each in response.xpath('//*[@id="screening"]/div[2]/ul/li/ul'):
            item = StartMeta()
            item['id'] = str(each.xpath('./li[1]/a/@href')[0]).split('/')[-1][:7]
            item['title'] = each.xpath('./li[1]/a/img/@alt')[0].extract()
            item['rate'] = '暂无评分' if not each.xpath('./li[3]/span[2]/text()')  \
                else each.xpath('./li[3]/span[2]/text()')[0].extract()
            item['url'] = each.xpath('./li[1]/a/@href')[0].extract()
            yield item



