# codding: utf-8
import re
from urllib.parse import urljoin
from spider.stagetwo.public.html_downloader import downloader_from_url

from bs4 import BeautifulSoup, Tag, NavigableString


class SguHtmlParser(object):
    def __init__(self, page_url, html_content):
        # 错误判断
        if page_url is None or str(page_url).strip() == "":
            raise Exception("SguHtmlParser: url不可为空")
        if html_content is None or str(html_content, encoding="windows-1251").strip() == "":
            raise Exception("SguHtmlParser: 内容不可为空")

        self.page_url = page_url
        if page_url.find("#"):
            self.page_url = page_url.split("#")[0]
        self.html_content = html_content
        self.str_html_content = str(html_content, encoding="windows-1251").replace("<br>", "<br />")
        self.soup = BeautifulSoup(self.str_html_content, "html.parser", from_encoding="windows-1251")
        if self.soup.find('h4',text="no such problem"):
            raise Exception("SguHtmlParser: 此题不存在")
        pass

    def get_urls(self):
        if self.page_url.find("volume") < 0:
            return set()

        new_urls = set()
        links = self.soup.find_all('a', href=re.compile(r"(contest=\d+&volume=\d+$)|(contest=\d+&problem=\d+$)"))
        for tag in links:
            t_url = tag['href']
            t_url = urljoin(self.page_url, t_url)
            new_urls.add(t_url)
        return new_urls
        pass

    def get_problem(self):
        # 如果不是问题页面, 返回None
        if self.page_url.find("problem=") < 0:
            return None

        # 重置所有图片链接
        imgs = self.soup.find_all('img')
        for img in imgs:
            # print(urljoin(page_url, img['src']))
            img['src'] = urljoin(self.page_url, img['src'])

        imgs = self.soup.find_all('image')
        for img in imgs:
            # print(urljoin(page_url, img['src']))
            img['src'] = urljoin(self.page_url, img['src'])

        res_data = {"url": self.page_url, "ojname": "Sgu"}
        if self.page_url.find(".html") < 0:
            res_data["sourceid"] = re.compile("\d+$").findall(self.page_url)[0]
        else:
            res_data["sourceid"] = ""
        res_data["source"]=""
        self._get_content_data(res_data)

        return res_data
        pass

    def get_status(self):
        return None
        pass

    def _get_content_data(self, res_data):
        """从页面中提取信息"""
        # 时间限制
        tag = self.soup.find(text=re.compile("time\s+limit", flags=re.IGNORECASE))
        res_data["time_limit"] = str(tag).split(":")[-1].replace("\\n", "").strip().replace("\\r", "")

        # 题目名称
        # print(tag.parent.name)
        # print(tag.parent.parent.name)
        # return None
        # while tag.parent.name != "[document]":# not isinstance(tag.parent, Tag) or tag.parent is None or tag.parent.name != "body":
        #     tag = tag.parent
        # print("-----------------------------------")
        # print(tag.name)
        # if tag.name == "[document]":
        #     print("is document")
        # else:
        #     print("is not document")
        # print(tag)
        # pass
        # tag = tag.parent.previous_sibling

        if tag.parent.next_sibling is None:
            tag = tag.parent.parent.previous_sibling
        else:
            tag = tag.parent.previous_sibling
        # 掠过 NavigableString
        while not isinstance(tag, Tag):
            tag = tag.previous_sibling
        # print(tag)
        # return None
        title_str = ""
        for string in tag.stripped_strings:
            title_str += str(string)
        if title_str.find(".") >= 0:
            res_data["title"] = title_str.split(".")[-1].strip().replace("\\n", "").replace("\\r", "")
        else:
            res_data["title"] = title_str.strip().replace("\\n", "").replace("\\r", "")

        # 内存限制
        tag = self.soup.find(text=re.compile("memory\s+limit", flags=re.IGNORECASE))
        res_data["memory_limit"] = str(tag).split(":")[-1].replace("\\n", "").replace("\\r", "").strip()
        # print(tag.parent.previous_sibling.previous_sibling)

        if tag.parent.next_sibling is None:
            tag = tag.parent.parent
        else:
            tag = tag.parent
        t_str = ""
        last_data = "description"
        # cnt = 1
        for sibling in tag.next_siblings:
            # print(str(sibling))
            # 如果是Tag变量,而且有Tag Children
            if isinstance(sibling, Tag) and len(sibling.contents) > 0:
                for child in sibling.children:
                    if self._judge_tag_equal_str(tag=child, string="input"):
                        # print("input,cnt:", cnt, last_data, "t_str:", t_str)
                        # cnt += 1
                        res_data[last_data] = t_str.replace("\\n", "").replace("\\r", "")
                        if "pinput" not in res_data:
                            last_data = "pinput"
                        else:
                            last_data = "sample_input"
                        t_str = ""
                        self._decompose_soup_element(child)
                        pass
                    elif self._judge_tag_equal_str(tag=child, string="output"):
                        # print("output,cnt:", cnt, last_data, "t_str:", t_str)
                        # cnt += 1
                        res_data[last_data] = t_str.replace("\\n", "").replace("\\r", "")
                        # print(last_data)
                        if "poutput" not in res_data:
                            last_data = "poutput"
                        else:
                            last_data = "sample_output"
                        t_str = ""
                        self._decompose_soup_element(child)
                        pass
                    elif self._judge_tag_equal_str(tag=child, string="sample input"):
                        # print("sample input,cnt:", cnt, last_data, "t_str:", t_str)
                        # cnt += 1
                        # print("sample input")
                        res_data[last_data] = t_str.replace("\\n", "").replace("\\r", "")
                        last_data = "sample_input"
                        t_str = ""
                        self._decompose_soup_element(child)
                        pass
                    elif self._judge_tag_equal_str(tag=child, string="sample output"):
                        # print("sample output,cnt:", cnt, last_data, "t_str:", t_str)
                        # cnt += 1
                        # print("sample output")
                        res_data[last_data] = t_str.replace("\\n", "").replace("\\r", "")
                        last_data = "sample_output"
                        t_str = ""
                        # print(child)
                        self._decompose_soup_element(child)
                        # print(type(child))
                        pass
                    elif self._judge_tag_equal_str(tag=child, string="note"):
                        # print("note,cnt:", cnt, last_data, "t_str:", t_str)
                        # cnt += 1
                        res_data[last_data] = t_str.replace("\\n", "").replace("\\r", "")
                        last_data = "hint"
                        t_str = ""
                        self._decompose_soup_element(child)
                        pass

                    elif self._judge_tag_equal_str(tag=child, string="Example(s)"):
                        # print("examples(s)", cnt, last_data, "t_str:", t_str)
                        # cnt += 1
                        res_data[last_data] = t_str.replace("\\n", "").replace("\\r", "")
                        last_data = "sample_input"
                        t_str = ""
                        self._decompose_soup_element(child)
                        pass
                    elif self._judge_tag_equal_str(tag=child, string="Sample test(s)"):
                        # print("Sample test(s),cnt:", cnt, last_data, "t_str:", t_str)
                        # cnt += 1
                        res_data[last_data] = t_str.replace("\\n", "").replace("\\r", "")
                        last_data = "sample_input"
                        t_str = ""
                        self._decompose_soup_element(child)
                        pass

                    elif self._is_hr(child):
                        # print("hr,cnt:", cnt, last_data, "t_str:", t_str)
                        # cnt += 1
                        res_data[last_data] = t_str.replace("\\n", "").replace("\\r", "")
                        t_str = ""
                        pass
                    pass
                pass
            t_str += str(sibling)
            pass
        res_data[last_data] = t_str.replace("\\n", "").replace("\\r", "")
        return
        pass

    @staticmethod
    def _judge_tag_equal_str(tag, string, ignorecase=True):
        if isinstance(tag, Tag):
            cmp_str = str(tag.text).strip()
        elif isinstance(tag, NavigableString):
            cmp_str = str(tag.string).strip()
            # print("cmp_str",cmp_str)
        else:
            return False
        if ignorecase:
            return cmp_str.lower() == str(string).lower()
        else:
            return cmp_str == string

    @staticmethod
    def _decompose_soup_element(child):
        if isinstance(child, Tag):
            child.decompose()
        elif isinstance(child, NavigableString):
            child.string = ""
        pass

    @staticmethod
    def _is_hr(child):
        if isinstance(child, Tag):
            return child.name == "hr"
        pass


if __name__ == "__main__":
    root_url = "http://acm.sgu.ru/problem.php?contest=0&problem=481"
    # root_url = "http://acm.sgu.ru/problemset.php?show_volumes"
    # root_url = "http://localhost:8080/oj/sgu/show_volumes.html"
    # root_url = "http://localhost:8080/oj/sgu/contest=0&volume=1.html"
    # root_url = "http://localhost:8080/oj/sgu/contest=0&problem=117.html"
    # root_url = "http://localhost:8080/oj/sgu/contest=0&problem=500.html"
    # root_url = "http://localhost:8080/oj/sgu/contest=0&problem=115.html"
    # root_url = "http://acm.sgu.ru/problem.php?contest=0&problem=378"
    # root_url = "http://acm.sgu.ru/problemset.php?show_volumes"
    # root_url = "http://acm.sgu.ru/problem.php?contest=0&problem=115"
    html_content = downloader_from_url(root_url)
    parser = SguHtmlParser(root_url, html_content)
    print(parser.get_problem())
    pass
