# coding: utf-8


class UrlManager():
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
        pass

    def add_new_url(self, url):
        if url is None:
            return
        # print("即将添加新URL:", url)
        if url not in self.new_urls and url not in self.old_urls:
            # print("成功添加新URL:", url)
            self.new_urls.add(url)
        pass

    def add_new_urls(self, urls):
        if urls is None or len(urls)==0:
            return
        for url in urls:
            self.add_new_url(url)
        pass

    def add_old_url(self, url):
        if url is None or url in self.old_urls:
            return
        # print("添加爬取过的URL:", url[0])
        if url in self.new_urls:
            self.new_urls.remove(url)
            pass
        self.old_urls.add(url)
        pass

    def add_old_urls(self, urls):
        if urls is None or len(urls)==0:
            return
        for url in urls:
            # print(type(url))
            self.add_old_url(url)
        pass

    def get_new_url(self):
        if not self.has_url():
            return None
        new_url = self.new_urls.pop()
        self.add_old_url(new_url)
        return new_url
        pass

    def has_url(self):
        return len(self.new_urls) != 0
        pass

    def new_urls_size(self):
        return len(self.new_urls)

    pass


if __name__ == "__main__":
    from spider.dboper.commondb import CommonDB
    db_hundler = CommonDB()
    db_hundler.execute("SELECT url FROM mixojapp_problem WHERE ojname='Poj'")
    res = db_hundler.fetchall()
    print(type(res))
    db_hundler.close()

    url_m = UrlManager()
    url_m.add_old_urls(res)

    url_m.add_new_url('http://poj.org/problem?id=1023')
    pass
