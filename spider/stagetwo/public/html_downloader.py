# coding: utf-8
import urllib
import urllib.request
import urllib.response
import random


class HtmlDownloader(object):
    @staticmethod
    def download(url):
        if url is None:
            return None
        usera=[
               'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
               'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)'

        ]
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
        }
        index=random.randint(0,4)
        header = { 'User-Agent' : usera[index]}
        try:
           req = urllib.request.Request(url, None, headers=header)
           res = urllib.request.urlopen(req, timeout=5)
           if res.getcode() != 200:
             print("下载页面 %s 失败." % url)
             return None
           return res.read()
        except Exception as e:
            print(e)

        pass
    pass


def downloader_from_url(url):
    url_downloader = HtmlDownloader()
    return url_downloader.download(url)
    pass

if __name__=="__main__":
    downloader = HtmlDownloader()
    for i in range(1,20):
        downloader.download("http://acm.timus.ru/problem.aspx?space=1&num=1000")
        print("ok")
    pass
