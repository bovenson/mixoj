# codding: utf-8
import re
from queue import Queue
from urllib.parse import urljoin
from spider.stageone.public.html_downloader import downloader_from_url
from bs4 import BeautifulSoup


class ZojHtmlParser(object):
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
        self.str_html_content = str(html_content, encoding="utf-8")
        self.soup = BeautifulSoup(html_content, "html.parser", from_encoding="utf-8")
        pass

    def get_urls(self):
        """得到页面中需要的链接"""
        new_urls = set()
        links = self.soup.find_all('a',
                                   href=re.compile(r'(showProblems.do\?contestId=\d+&pageNumber=\d+$)|'
                                              r'(showProblem.do\?problemCode=\d+$)'))
        # print(links)
        for tag in links:
            t_url = tag['href']
            t_url = urljoin(self.page_url, t_url)
            new_urls.add(t_url)
        return new_urls
        pass

    def get_problem(self):
        """提取页面数据"""
        # 如果不是问题页面,不再提取数据
        if self.page_url.find("problemCode=") < 0:
            return None

        # 重置所有图片链接
        imgs = self.soup.find_all('img')
        # print(imgs)
        for img in imgs:
            img['src'] = urljoin(self.page_url, img['src'])


        new_data = {"sourceid": re.compile("\d+$").findall(self.page_url)[0], "url": self.page_url, "ojname": "Zoj",
                    "title": str(self.soup.find("span", class_="bigProblemTitle").text),
                    "time_limit": str(re.compile("\d+").findall(self.soup.find("font",
                                                                               text=re.compile("Time Limit:")).next_sibling)[0]) + "S",
                    "memory_limit": str(re.compile("\d+").findall(self.soup.find("font", text=re.compile("Memory Limit:")).next_sibling)[0]) + "K"}
        # print(new_data["sourceid"])

        content_data = self._get_content(self.soup)
        new_data["description"] = content_data["description"]
        new_data["pinput"] = content_data["pinput"]
        new_data["poutput"] = content_data["poutput"]
        new_data["sample_input"] = content_data["sample_input"]
        new_data["sample_output"] = content_data["sample_output"]
        new_data["hint"] = ""
        new_data["source"] = content_data["source"]

        return new_data
        pass

    def get_status(self):
        status_url = re.compile("/onlinejudge/showProblemStatus\.do\?problemId=\d+").findall(self.str_html_content)
        if len(status_url) == 0:
            return None
        full_url = urljoin(self.page_url, status_url[0])
        # 下载数据页
        statistic_html_content = str(downloader_from_url(full_url), encoding="utf-8")
        # 解析数据页
        # print(statistic_html_content)
        items_to_find = {
            "AC": "ac",
            "WA": "wa",
            "PE": "pe",
            "FPE": "fpe",
            "SF": "sf",
            "NZEC": "nzec",
            "TLE": "tle",
            "MLE": "mle",
            "CE": "ce",
            "SE": "se",
            "RE": "re",
            "Total": "total_sub",
        }
        # 处理错误项名称
        statistic_find_items = []
        for item in re.findall(r"<td[^>]+>\s*[A-Za-z]+\s*</td>", statistic_html_content):
            t_find = re.findall(r">\s*[A-Za-z]+\s*<", item)
            if len(t_find) > 0:
                t_find = t_find[0].replace(">", "").replace("<", "").strip()
                if t_find in items_to_find.keys():
                    statistic_find_items.append(t_find)
                    pass
                    # print(t_find)
        statistic_find_nums = []
        for statistic_find_num in re.findall(r"(<a[^>]+>\d+\(\d+%\)</a>)|(<a[^>]+>\d+</a>)", statistic_html_content):
            for i in statistic_find_num:
                if len(i) != 0 and str(i).find("problemCode=") > 0:
                    i = re.sub("<a[^>]*>", "", i)
                    i = re.sub("\(\d+%\)", "", i)
                    i = re.sub("</a>", "", i).strip()
                    statistic_find_nums.append(i)
                    # print(i)
        min_len = min(len(statistic_find_items), len(statistic_find_nums))
        data_cont = dict()
        for i in range(min_len):
            db_name = items_to_find[statistic_find_items[i]]
            data_cont[db_name] = statistic_find_nums[i]
        return data_cont
        # print(statistic_find_nums)
        pass

    @staticmethod
    def _get_content(soup):
        content_data = {"description": "", "pinput": "", "poutput": "", "sample_input": "", "sample_output": "",
                        "source": ""}

        # t_str = ""

        # content_body = soup.find("div", id="content_body")
        # print(str(content_body))
        # print(re.compile("Input").findall(str(content_body)))
        # print(len(str(content_body).split("</center>")))
        # print(str(content_body).split("</center>")[2])
        t_content = ""
        # for t_str in str(html_content, encoding="utf-8").split("</center>")[2:]:
        for t_str in str(soup).split("</center>")[2:]:
            t_content += t_str
            pass

        # 重置所有图片链接
        # print(t_content)
        # page_img = re.compile("<img src=.*[0-9]+\s*>", flags=re.IGNORECASE).findall(t_content)
        # for img in page_img:
        #     print(img)
        #     imgsoup = BeautifulSoup(img, "html.parser", from_encoding="utf-8").find('img')
        #     full_url = urljoin(page_url, imgsoup['src'])
        #     imgsoup['src'] = full_url
        #     t_content.replace("IMG", str(imgsoup))

        # spider.public.writetofile.write_str_to_file(t_content)
        # if len(re.compile("<b>Input(</h4>)|(</b>)").findall(content)) > 0:
        q = Queue()
        q.put("description")
        # print(t_content)
        re_common = "<b>(\s)*%s[a-z]{0,2}(\s)*[a-zA-Z]{0,15}(\s)*</b>"
        if len(re.compile("<h4>(\s)*[a-zA-Z]{0,15}(\s)*Input(\s)*[a-zA-Z]{0,15}(\s)*</h4>",
                          flags=re.IGNORECASE).findall(t_content)) > 0:
            re_common = "<h4>(\s)*%s[a-z]{0,2}(\s)*[a-zA-Z]{0,15}(\s)*</h4>"
        if len(re.compile("<h3>(\s)*[a-zA-Z]{0,15}(\s)*Input(\s)*[a-zA-Z]{0,15}(\s)*</h3>",
                          flags=re.IGNORECASE).findall(t_content)) > 0:
            re_common = "<h3>(\s)*%s[a-z]{0,2}(\s)*[a-zA-Z]{0,15}(\s)*</h3>"
        if len(re.compile("<h5>(\s)*[a-zA-Z]{0,15}(\s)*Input(\s)*[a-zA-Z]{0,15}(\s)*</h5>",
                          flags=re.IGNORECASE).findall(t_content)) > 0:
            re_common = "<h5>(\s)*%s[a-z]{0,2}(\s)*[a-zA-Z]{0,15}(\s)*</h5>"
        if len(re.compile("<h2>(\s)*[a-zA-Z]{0,15}(\s)*Input(\s)*[a-zA-Z]{0,15}(\s)*</h2>",
                          flags=re.IGNORECASE).findall(t_content)) > 0:
            re_common = "<h2>(\s)*%s[a-z]{0,2}(\s)*[a-zA-Z]{0,15}(\s)*</h2>"
        # print("使用匹配规则:", re_common % "ssss")
        #
        # re_common = "(<b>(\s)*[a-zA-Z]{0,15}(\s)*%s(\s)*[a-zA-Z]{0,15}(\s)*</b>)|" \
        #             "(<h4>(\s)*[a-zA-Z]{0,15}(\s)*%s(\s)*[a-zA-Z]{0,15}(\s)*</h4>)"
        # re_common = "((<h4>)|(<b>))(\s)*%s(\s)*(</h4>)|(</b>)"
        t_re_res = re.split(re_common.replace("%s", "Input"), t_content, flags=re.IGNORECASE)
        if len(t_re_res) > 1:
            last_dec = str(q.get())
            content_data[last_dec] = t_re_res[0]
            t_content = ""
            for t in t_re_res[1:]:
                if t is not None:
                    t_content += t
            q.put("pinput")
            t_content.replace("</p>", "", 1)
            if len(re.compile("<p>\s*$").findall(content_data[last_dec])) > 0:
                content_data[last_dec] += "</p>"
                pass
            # print("description:", content_data["description"])
            pass

        # print(t_content)
        t_re_res = re.split(re_common.replace("%s", "Output"), t_content, flags=re.IGNORECASE)
        if len(t_re_res) > 1:
            last_dec = str(q.get())
            content_data[last_dec] = t_re_res[0]
            t_content = ""
            for t in t_re_res[1:]:
                if t is not None:
                    t_content += t
            q.put("poutput")
            if len(re.compile("<p>\s*$").findall(content_data[last_dec])) > 0:
                content_data[last_dec] += "</p>"
                pass
            # print("pinput:", content_data["pinput"])
            pass

        # print("content:\n", t_content)
        # print("使用的re:\n", re_common.replace("%s", "Sample Input"))
        t_re_res = re.split(re_common.replace("%s", "Sample Input"), t_content, flags=re.IGNORECASE)
        if len(t_re_res) > 1:
            last_dec = q.get()
            content_data[last_dec] = t_re_res[0]
            t_content = ""
            for t in t_re_res[1:]:
                if t is not None:
                    t_content += t
            q.put("sample_input")
            if len(re.compile("<p>\s*$").findall(content_data[last_dec])) > 0:
                content_data[last_dec] += "</p>"
                pass
            # print("poutput:", content_data["poutput"])
            pass

        t_re_res = re.split(re_common.replace("%s", "Sample Output"), t_content, flags=re.IGNORECASE)
        if len(t_re_res) > 1:
            last_dec = str(q.get())
            content_data[last_dec] = t_re_res[0]
            t_content = ""
            for t in t_re_res[1:]:
                if t is not None:
                    t_content += t
                    pass
                pass
            # t_content.replace("</p>", "", 1)
            q.put("sample_output")
            if len(re.compile("<p>\s*$").findall(content_data[last_dec])) > 0:
                content_data[last_dec] += "</p>"
                pass
            # print("sample_input:", content_data["sample_input"])
            pass

        t_re_res = re.split("(Contest:)|(Author:)|(Source:)\s*<strong>", t_content, flags=re.IGNORECASE)
        if len(t_re_res) > 1:
            last_dec = str(q.get())
            content_data[last_dec] = t_re_res[0]
            t_content = ""
            for t in t_re_res[1:]:
                if t is not None:
                    t_content += t
                    pass
                pass
            q.put("source")
            if len(re.compile("<p>\s*$").findall(content_data[last_dec])) > 0:
                content_data[last_dec] += "</p>"
                pass
            # print("sample_output:", content_data["sample_output"])
            # print(t_content)
            pass

        t_re_res = re.split("</strong>(<br>)*\s*<center>", t_content, flags=re.IGNORECASE)
        if len(t_re_res) > 1:
            last_dec = str(q.get())
            content_data[last_dec] = t_re_res[0]
            t_content = ""
            for t in t_re_res[1:]:
                if t is not None:
                    t_content += t
                    pass
                pass
            if len(re.compile("<p>\s*$").findall(content_data[last_dec])) > 0:
                content_data[last_dec] += "</p>"
                pass
            # print("source:\n", content_data["source"])
            pass

        content_data['source'].replace("<strong>", "")
        content_data['source'].replace("</strong>", "")
        content_data['source'].replace("<br>", "\n")
        # print(content_data["description"])
        # for tstr in str(content_body).split("<hr>"):
        #    print(tstr)
        # print("*****************")
        # cnt = 0
        # description_flag = False
        # for tag in content_body.children:
        #     if str(tag).isspace():
        #         continue
        #     cnt += 1
        #     if cnt < 3:
        #         continue
        #         pass
        #     # print("type:", type(tag))
        #     # print("tag name:", tag.name)
        #     # print(str(tag))
        #
        #     if isinstance(tag, bs4.element.Tag) and tag.name == "p":
        #         # print("进入判断")
        #         # print(str(tag))
        #         # 找Description
        #         t_tag = tag.find('b', text=re.compile("Input"))
        #         if t_tag is not None and str(t_tag.text).strip() == "Input":
        #             t_tag.decompose()
        #             content_data["description"] = t_str
        #             t_str = ""
        #             pass
        #             # print("find input:", str(tag.find('b', text="Input")))
        #         # 找输入描述
        #         t_tag = tag.find('b', text=re.compile("Output"))
        #         if t_tag is not None and str(t_tag.text).strip() == "Output":
        #             t_tag.decompose()
        #             if description_flag is False:
        #                 content_data["description"] = t_str
        #             else:
        #                 content_data["pinput"] = t_str
        #             t_str = ""
        #             pass
        #         # 找输出描述
        #         t_tag = tag.find('b', text=re.compile("Sample Input"))
        #         if t_tag is not None and str(t_tag.text).strip() == "Sample Input":
        #             t_tag.decompose()
        #             if description_flag is False:
        #                 content_data["description"] = t_str
        #             else:
        #                 content_data["poutput"] = t_str
        #             t_str = ""
        #             pass
        #         # 找样例输入
        #         t_tag = tag.find('b', text=re.compile("Sample Output"))
        #         if t_tag is not None and str(t_tag.text).strip() == "Sample Output":
        #             t_tag.decompose()
        #             if description_flag is False:
        #                 content_data["description"] = t_str
        #             else:
        #                 content_data["sample_input"] = t_str
        #             t_str = ""
        #             pass
        #     # 找样例输出
        #     if tag.name is None and str(tag).strip() == "Source:":
        #         if description_flag is False:
        #             content_data["description"] = t_str
        #         else:
        #             content_data["sample_output"] = t_str
        #         t_str = ""
        #         # 找到source
        #         content_data["source"] = str(tag.next_sibling.text)
        #         pass
        #     t_str += str(tag)
        #     # ("****************************************************")
        return content_data
        pass

if __name__ == "__main__":
    root_url = "http://acm.zju.edu.cn/onlinejudge/showProblem.do?problemCode=1006"
    html_content = downloader_from_url(root_url)
    parser = ZojHtmlParser(root_url, html_content)
    print(parser.get_status())
    pass
