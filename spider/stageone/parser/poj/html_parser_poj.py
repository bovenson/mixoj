# coding: utf-8
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from spider.stageone.public.str_process import strip_useless_html_tag
from spider.stageone.public.html_downloader import downloader_from_url


class PojHtmlParser(object):
    def __init__(self, page_url, html_content):
        # 错误判断
        if page_url is None or str(page_url).strip() == "":
            raise Exception("PojHtmlParser: url不可为空")
        if html_content is None or str(html_content, encoding="utf-8").strip() == "":
            raise Exception("PojHtmlParser: 内容不可为空")

        self.page_url = page_url
        if page_url.find("#"):
            self.page_url = page_url.split("#")[0]
        self.html_content = html_content
        self.str_html_content = str(html_content)
        self.soup = BeautifulSoup(html_content, "html.parser", from_encoding="utf-8")
        pass

    def get_urls(self):
        """从页面中提取有用的URL"""
        new_urls = set()
        links = self.soup.find_all('a', href=re.compile(r"(^problemlist\?volume=\d+$)|"
                                                        r"(^problem\?id=\d+$)"))
        # r"(^problemstatus\?problem_id=\d+$)"))
        for tag in links:
            t_url = tag['href']
            t_url = urljoin(self.page_url, t_url)
            new_urls.add(t_url)
        return new_urls

    def get_problem(self):
        """从网页中提取题目数据"""
        # 如果当前url是列表,不提取数据
        if len(re.compile("poj\.org/problem\?id=\d+").findall(self.page_url)) == 0:
            return None

        # 重置所有图片链接
        imgs = self.soup.find_all('img')
        # print(imgs)
        for img in imgs:
            img['src'] = urljoin(self.page_url, img['src'])
        # print(imgs)

        # 提取问题页内容
        res_data = {"url": self.page_url, "ojname": "Poj", "sourceid": re.compile("\d+$").findall(self.page_url)[0],
                    "title": str(self.soup.find("div", class_="ptt").text),
                    "time_limit": str(self.soup.find("b", text="Time Limit:").next_sibling),
                    "memory_limit": str(self.soup.find("b", text="Memory Limit:").next_sibling),
                    "description": str(self.soup.find("p", text="Description").next_sibling)}
        # print("得到sourceid:", res_data["sourceid"])

        tag = self.soup.find("p", text="Input")
        res_data["pinput"] = ""
        if tag is not None:
            res_data["pinput"] = strip_useless_html_tag(str(tag.next_sibling))
        # print("抓取的input:", res_data["pinput"])

        tag = self.soup.find("p", text="Output")
        res_data["poutput"] = ""
        if tag is not None:
            res_data["poutput"] = strip_useless_html_tag(str(tag.next_sibling))

        tag = self.soup.find("p", text="Sample Input")
        res_data["sample_input"] = ""
        if tag is not None:
            res_data["sample_input"] = strip_useless_html_tag(str(tag.next_sibling))

        tag = self.soup.find("p", text="Sample Output")
        res_data["sample_output"] = ""
        if tag is not None:
            res_data["sample_output"] = strip_useless_html_tag(str(tag.next_sibling))

        tag = self.soup.find("p", text="Hint")
        res_data["hint"] = ""
        if tag is not None:
            res_data["hint"] = strip_useless_html_tag(str(tag.next_sibling))

        tag = self.soup.find("p", text="Source")
        res_data["source"] = ""
        if tag is not None:
            res_data["source"] = strip_useless_html_tag(str(tag.next_sibling.find('a').text))

        return res_data
        pass

    def get_status(self):
        """得到当前问题的提交数据信息"""
        # 如果不是详情页, 返回None
        # 当前问题id
        find = re.compile("\d+$").findall(self.page_url)
        if len(find) == 0:
            return None
        pid = find[0]
        # 数据页 url
        statistics_page_url = urljoin(self.page_url, "problemstatus?problem_id="+pid)
        statistics_html_content = str(downloader_from_url(statistics_page_url))

        statistics = {}
        last = 0
        # Accepted
        find = re.compile("sa\[0\]\[" + str(last) + "\]\s*=\s*\d+",
                          flags=re.IGNORECASE).findall(statistics_html_content)
        if len(find) != 0:
            last += 1
            statistics["ac"] = find[0].split("=")[-1].strip()

        # Presentation Error
        find = re.compile("sa\[0\]\[" + str(last) + "\]\s*=\s*\d+",
                          flags=re.IGNORECASE).findall(statistics_html_content)
        if len(find) != 0:
            last += 1
            statistics["pe"] = find[0].split("=")[-1].strip()

        # Time Limit Exceeded
        find = re.compile("sa\[0\]\[" + str(last) + "\]\s*=\s*\d+",
                          flags=re.IGNORECASE).findall(statistics_html_content)
        if len(find) != 0:
            last += 1
            statistics["tle"] = find[0].split("=")[-1].strip()

        # Memory Limit Exceeded
        find = re.compile("sa\[0\]\[" + str(last) + "\]\s*=\s*\d+",
                          flags=re.IGNORECASE).findall(statistics_html_content)
        if len(find) != 0:
            last += 1
            statistics["mle"] = find[0].split("=")[-1].strip()

        # Wrong Answer
        find = re.compile("sa\[0\]\[" + str(last) + "\]\s*=\s*\d+",
                          flags=re.IGNORECASE).findall(statistics_html_content)
        if len(find) != 0:
            last += 1
            statistics["wa"] = find[0].split("=")[-1].strip()

        # Runtime Error
        find = re.compile("sa\[0\]\[" + str(last) + "\]\s*=\s*\d+",
                          flags=re.IGNORECASE).findall(statistics_html_content)
        if len(find) != 0:
            last += 1
            statistics["re"] = find[0].split("=")[-1].strip()

        # Output Limit Exceeded
        find = re.compile("sa\[0\]\[" + str(last) + "\]\s*=\s*\d+",
                          flags=re.IGNORECASE).findall(statistics_html_content)
        if len(find) != 0:
            last += 1
            statistics["ole"] = find[0].split("=")[-1].strip()

        # Compile Error
        find = re.compile("sa\[0\]\[" + str(last) + "\]\s*=\s*\d+",
                          flags=re.IGNORECASE).findall(statistics_html_content)
        if len(find) != 0:
            last += 1
            statistics["ce"] = find[0].split("=")[-1].strip()

        # System Error
        find = re.compile("sa\[0\]\[" + str(last) + "\]\s*=\s*\d+",
                          flags=re.IGNORECASE).findall(statistics_html_content)
        if len(find) != 0:
            last += 1
            statistics["se"] = find[0].split("=")[-1].strip()

        # Waiting
        find = re.compile("sa\[0\]\[" + str(last) + "\]\s*=\s*\d+",
                          flags=re.IGNORECASE).findall(statistics_html_content)
        if len(find) != 0:
            last += 1
            statistics["waiting"] = find[0].split("=")[-1].strip()
        # Compiling
        find = re.compile("sa\[0\]\[" + str(last) + "\]\s*=\s*\d+",
                          flags=re.IGNORECASE).findall(statistics_html_content)
        if len(find) != 0:
            last += 1
            statistics["compiling"] = find[0].split("=")[-1].strip()

        total_sub = 0
        for key in statistics.keys():
            total_sub += int(statistics[key])
            pass
        statistics['total_sub'] = total_sub
        user_info = re.compile("200\s*,250\s*,\s*\d+\s*,\s*\d+").findall(statistics_html_content)[0].split(",")
        # print(user_info[-1])
        # print(user_info[-2])
        # Users (Submitted)
        statistics['user_sub'] = user_info[-2].strip()
        # Users (Solved)
        statistics['user_ac'] = user_info[-1].strip()
        # Total Submissions
        # print(",".join([str(total_sub), user_sub, user_ac, ac, pe, tle, mle, wa, pre, ole, ce, se, waiting]))
        # print(self.soup.prettify())
        # statistics = {
        #     "total_sub": total_sub,
        #     "user_sub": user_sub,
        #     "user_ac": user_ac,
        #     "ac": ac,
        #     "pe": pe,
        #     "tle": tle,
        #     "mle": mle,
        #     "wa": wa,
        #     "pre": pre,
        #     "ole": ole,
        #     "ce": ce,
        #     "se": se,
        #     "waiting": waiting,
        # }
        statistics['ojname'] = "Poj"
        statistics['sourceid'] = re.compile("\d+$").findall(self.page_url)[0]
        return statistics
        pass


if __name__ == "__main__":
    # purl = "http://poj.org/problem?id=1005"
    # purl = "http://poj.org/problemstatus?problem_id=1001"
    purl = "http://poj.org/problem?id=1085#top"
    # purl = "http://poj.org/problemlist"
    from spider.public.html_downloader import downloader_from_url

    html_cont = downloader_from_url(purl)
    parser = PojHtmlParser(purl, html_cont)
    print(parser.get_status())
    # import urllib
    # import urllib.request
    #
    # url = "http://poj.org/problemlist?volume=1"
    # res = urllib.request.urlopen(url, timeout=5)
    # poj_parser = PojHtmlParser()
    # t_urls, new_data = poj_parser.parser(url, res.read())
    # print("当前url:", url)
    # print("提取到的url:", t_urls)
    # print("提取到的数据:", new_data)
    #
    # print("***********************************************************")
    #
    # url = "http://poj.org/problem?id=1957"
    # res = urllib.request.urlopen(url, timeout=5)
    # poj_parser = PojHtmlParser()
    # t_urls, new_data = poj_parser.parser(url, res.read())
    # print("当前url:", url)
    # print("提取到的url:", t_urls)
    # print("提取到的数据:", new_data)
    pass
