# coding: utf-8
import urllib
import urllib.request
import urllib.response


class HtmlDownloader(object):
    @staticmethod
    def download(url):
        if url is None:
            return None

        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
        }

        req = urllib.request.Request(url, None, headers)
        res = urllib.request.urlopen(req, timeout=5)
        if res.getcode() != 200:
            print("下载页面 %s 失败." % url)
            return None
        # print("下载页面 %s 成功." % url)

        return res.read()
        pass
    pass


def downloader_from_url(url):
    url_downloader = HtmlDownloader()
    return url_downloader.download(url)
    pass

if __name__=="__main__":
    downloader = HtmlDownloader()
    cont = downloader.download("https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8&category=679&page=show_problem&problem=5576")
    # cont = downloader.download("https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=5576")
    print(cont)
    # for i in range(1,20):
    #     downloader.download("http://acm.timus.ru/problem.aspx?space=1&num=1000")
    #     print("ok")
    pass
