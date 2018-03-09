import re
from urllib.parse import urljoin
from spider.stagetwo.public.html_downloader import downloader_from_url
import spider.stagetwo.public.html_downloader
from spider.stagetwo.public.str_process import strip_useless_html_tag
from bs4 import BeautifulSoup, Tag, NavigableString


class HysbzHtmlParser(object):
    def __init__(self, page_url, html_content):
        if page_url is None or str(page_url).strip() == "":
            raise Exception("HysbzHtmlParser: url不可为空")
        if html_content is None or str(html_content, encoding="utf-8").strip() == "":
            raise Exception("HysbzHtmlParser: 内容不可为空")
        self.page_url = page_url
        if page_url.find("problemset"):
            self.page_url = page_url.split("problemset")[0]
        self.html_content = html_content
        # 转换成字符串格式
        self.str_html_content = str(html_content)
        self.soup = BeautifulSoup(html_content, "html.parser", from_encoding="utf-8")
        if self.soup.find(text="Please contact lydsy2012@163.com!"):
            raise Exception("HysbzHtmlParser: 此题不存在")

        pass

    def get_urls(self):
        new_urls = set()
        links = self.soup.find_all('a', href=re.compile(r"(^problemset.php\?page=\d+$)|"
                                                        r"(^problem.php\?id=\d+$)"))
        for tag in links:
            t_url = tag['href']
            t_url = urljoin(self.page_url, t_url)
            new_urls.add(t_url)

        return new_urls

    def get_problem(self):
        if self.page_url.find("http://www.lydsy.com/JudgeOnline/problem.php?id=") < 0:
            return None
        imgs = self.soup.find_all('img')
        # print(imgs)
        for img in imgs:
            img['src'] = urljoin(self.page_url, img['src'])

        imgs = self.soup.find_all('image')
        for img in imgs:
            # print(urljoin(page_url, img['src']))
            img['src'] = urljoin(self.page_url, img['src'])
        res_data = {"url": self.page_url, "ojname": "Hysbz"}
        res_data["sourceid"] = re.compile(r"\d+").findall(self.page_url)[0]
        title = str(self.soup.find("title").find_next("h2").text)
        res_data["title"] = re.split(re.compile(r"\d+:"), title)[1]
        s = strip_useless_html_tag(str(self.soup.find(text=re.compile("\d\sSec"))))
        res_data["time_limit"] = str(re.findall(re.compile(r"\d+"), s)[0]) + 'S'
        ss = strip_useless_html_tag(str(self.soup.find(text=re.compile("\d\sMB"))))
        res_data["memory_limit"] = str(re.findall(re.compile(r"\d+"), ss)[0]) + "MB"
        res_data["description"] = ""
        try:
            a = self.soup.find(text="Description").find_next("div")
            res_data["description"] = str(a)

        except:
            pass
        try:
            b = self.soup.find(text="Input").find_next("div")
            res_data["pinput"] = str(b)
        except:
            res_data["pinput"] = ""
            pass
        try:
            c = self.soup.find(text="Output").find_next("div")
            res_data["poutput"] = str(c)
        except:
            res_data["poutput"] = ""
            pass
        try:
            res_data["sample_input"] = str(self.soup.find(text="Sample Input").find_next("div"))
        except:
            res_data["sample_input"] = ""
        try:
            res_data["sample_output"] = str(self.soup.find(text="Sample Output").find_next("div"))
        except:
            res_data["sample_output"] = ""
        try:
            res_data["hint"] = str(self.soup.find(text="HINT").find_next("div"))
        except:
            res_data["hint"] = ""
        try:
            res_data["source"] = str(self.soup.find(text="Source").find_next("div"))
        except:
            res_data["source"] = ""
        return res_data

    def get_status(self):
        if self.page_url.find("http://www.lydsy.com/JudgeOnline/problem.php?id=") < 0:
            return None
        pid = re.compile(r"\d+").findall(self.page_url)[0]
        statistics_page_url = "http://www.lydsy.com/JudgeOnline/problemstatus.php?id=" + str(pid)
        statistics_html_content = downloader_from_url(statistics_page_url)
        statistics_soup = BeautifulSoup(statistics_html_content, "html.parser", from_encoding="utf-8")
        statistics = {}
        statistics["ojname"] = "Hysbz"
        statistics["sourceid"] = pid
        try:
            statistics["total_sub"] = statistics_soup.find(text="Submit").next.text
        except:
            statistics["total_sub"] = ""
        try:
            statistics["user_sub"] = statistics_soup.find(text="User(Submit)").next.text
        except:
            statistics["user_sub"] = ""
        try:
            statistics["user_ac"] = statistics_soup.find(text="User(Solved)").next.text
        except:
            statistics["user_ac"] = ""
        try:
            statistics["ac"] = statistics_soup.find(text="AC").next.text
        except:
            statistics["ac"] = ""
        try:
            statistics["wa"] = statistics_soup.find(text="WA").next.text
        except:
            statistics["wa"] = ""
        try:
            statistics["tle"] = statistics_soup.find(text="TLE").next.text
        except:
            statistics["tle"] = ""
        try:
            statistics["mle"] = statistics_soup.find(text="MLE").next.text
        except:
            statistics["mle"] = ""
        try:
            statistics["re"] = statistics_soup.find(text="RE").next.text
        except:
            statistics["re"] = ""
        try:
            statistics["ce"] = statistics_soup.find(text="CE").next.text
        except:
            statistics["ce"] = ""
        return statistics

        pass


if __name__ == "__main__":
    # uurl = "http://www.lydsy.com/JudgeOnline/problemset.php?page=2"
    uurl = "http://www.lydsy.com/JudgeOnline/problem.php?id=4129"
    html_cont = downloader_from_url(uurl)
    paser = HysbzHtmlParser(uurl, html_cont)
    paser.get_problem()
