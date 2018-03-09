# codding: utf-8
from urllib.parse import urljoin
import re
from bs4 import BeautifulSoup
from spider.stageone.public.html_downloader import downloader_from_url
from spider.stageone.public.str_process import strip_useless_html_tag


class UVALiveHtmlParser(object):
    def __init__(self, page_url, html_content):
        # 错误判断
        if page_url is None or str(page_url).strip() == "":
            raise Exception("UVALiveHtmlParser: url不可为空")
        if html_content is None or str(html_content, encoding="utf-8").strip() == "":
            raise Exception("UVALiveHtmlParser: 内容不可为空")

        self.page_url = page_url
        # 去掉网址标签
        if page_url.find("#"):
            self.page_url = page_url.split("#")[0]
        self.html_content = html_content
        self.str_html_content = str(html_content)
        self.soup = BeautifulSoup(html_content, "html.parser", from_encoding="utf-8")
        # print(self.soup.prettify())
        pass

        # 得到新的待爬取的url

    def get_urls(self):
        if self.page_url.find("show_problem&problem=") >= 0:
            return {}
        new_urls = set()
        links = self.soup.find_all('a', href=re.compile(r"(option=com_onlinejudge&Itemid=\d+&category=\d+$)|"
                                                        r"(option=com_onlinejudge&Itemid=\d+&category=\d+&"
                                                        r"page=show_problem&problem=\d+)"))
        for tag in links:
            t_url = tag['href']
            t_url = urljoin(self.page_url, t_url)
            new_urls.add(t_url)
        return new_urls
        pass

    # 从抓取的html中提取数据
    def get_problem(self):
        if self.page_url.find("problem=") < 0:
            return None
        res_data = {"url": self.page_url, "ojname": "UVALive", "sourceid": re.compile("\d+$").findall(self.page_url)[0]}
        # 得到source
        try:
            source = self.soup.find('td', class_='maincontent').find('table').find_all("tr")
            source = list(source)[1]
            source = source.find_all('a')
            source_list = list()
            for t_source in source:
                t_source_str = str(t_source.text).strip()
                if t_source_str not in source_list:
                    source_list.append(t_source_str)
            source_str = ",".join(source_list)
            # for source in source_set:
            #     source_str += str(source) + ","
            res_data["source"] = source_str
            # print(source_str)
            pass
        except:
            pass
        # 提取题目
        t_title = re.compile("<h[0-9]>\s*\d+\s*-\s*.*</h[0-9]>").findall(self.str_html_content)[0]
        # 去掉标签
        t_title = re.sub("</?h[0-9]>", "", t_title, flags=re.IGNORECASE)
        # if t_title.find("-") < 0:
        #     t_title = t_title.strip()
        # else:
        #     t_title = t_title.split("-", 1)[1].strip()
        res_data["title"] = t_title

        # 提取时限
        res_data["time_limit"] = (re.compile("Time\s+limit\s*:\s*\d+\.*\d*\s*[a-zA-z]+",
                                             flags=re.IGNORECASE).findall(self.str_html_content)[0]).split(":", 1)[
            1].strip()

        # 提取包含题目的iframe
        if self.soup.find('iframe') is None:
            raise Exception("没有找到题目内容")
        problem_url = urljoin(self.page_url, self.soup.find('iframe')['src'])
        # print(problem_url)
        problem_cont = str(downloader_from_url(url=problem_url), encoding="utf-8")
        # print(problem_url)
        # print(problem_cont)
        # return res_data

        # 判断题目是否以pdf页面显示
        t_data_find = re.compile("url=[a-z0-9]+\.pdf", flags=re.IGNORECASE).findall(problem_cont)
        if len(t_data_find) > 0:
            # 更改pdf的链接
            # pdf_url = t_data_find[0].replace("url=", "").replace("URL=", "")
            # full_url = urljoin(problem_url, pdf_url)
            # print(full_url)
            # problem_cont = re.sub("url=[a-z0-9]+\.pdf", "URL=" + full_url, string=problem_cont, flags=re.IGNORECASE)
            # print(problem_cont)


            res_data["description"] = '<iframe src="' + problem_url + '" width="100%" height="1000"scrolling="auto" ' \
                                                                      'frameborder="0">Unsupported browser.</iframe>'
            return res_data
            pass

        t_find_body = re.compile("<body[\s|\S]+</body>").findall(problem_cont)
        if len(t_find_body) == 0:
            prob_cont_body = problem_cont
            pass
        else:
            prob_cont_body = t_find_body[0]
            pass
        # print(cont_body)
        # 去掉body标签
        prob_cont_body = re.sub("<body[^>]*>", "", string=prob_cont_body, count=1, flags=re.IGNORECASE)
        prob_cont_body = re.sub("</body>", "", string=prob_cont_body, count=1, flags=re.IGNORECASE)
        # print(prob_cont_body)

        # 重置所有图片链接
        # print(re.compile("<img[^>]*>", flags=re.IGNORECASE).findall(prob_cont_body))
        for imgtag in re.compile("<img[^>]*>", flags=re.IGNORECASE).findall(prob_cont_body):
            try:
                # 找到图片url
                img_re_exp = "src=\"\S+\""
                # print(imgtag)
                full_url = urljoin(problem_url,
                                   re.compile(img_re_exp, flags=re.IGNORECASE).findall(imgtag)[0].split('"')[1])
                full_url = "src=\"" + full_url + "\""
                # print(full_url)
                # 替换
                new_img_tag = re.sub(img_re_exp, full_url, imgtag, flags=re.IGNORECASE)
                # print(imgtag)
                # print(new_img_tag)
                # prob_cont_body = re.sub(imgtag, new_img_tag, string=prob_cont_body, flags=re.IGNORECASE)
                prob_cont_body = prob_cont_body.replace(imgtag, new_img_tag)
                pass
            except:
                pass

        # print(cont_body)
        last_data = "description"

        # 找Input
        t_re_exp = "[\s|\S]*<[a-z][^>]*>\s*input\s*</[a-z][^>]*>"
        # 提取数据
        t_data_find = re.compile(t_re_exp, flags=re.IGNORECASE).findall(prob_cont_body)
        if len(t_data_find) > 0:
            last_data_find = t_data_find[0]
            # 去除数据
            prob_cont_body = re.sub(t_re_exp, "", string=prob_cont_body, count=1, flags=re.IGNORECASE)
            # 处理数据
            t_re_exp = "<[a-z][^>]*>\s*input\s*</[a-z][^>]*>$"
            last_data_find = re.sub(t_re_exp, "", string=last_data_find, count=1, flags=re.IGNORECASE)
            last_data_find = strip_useless_html_tag(last_data_find)
            # 保存数据
            res_data[last_data] = last_data_find
            last_data = "pinput"

        # 找Output
        t_re_exp = "[\s|\S]*<[a-z][^>]*>\s*output\s*</[a-z][^>]*>"
        # 提取数据
        t_data_find = re.compile(t_re_exp, flags=re.IGNORECASE).findall(prob_cont_body)
        if len(t_data_find) > 0:
            last_data_find = t_data_find[0]
            # 去除数据
            prob_cont_body = re.sub(t_re_exp, "", string=prob_cont_body, count=1, flags=re.IGNORECASE)
            # 处理数据
            t_re_exp = "<[a-z][^>]*>\s*output\s*</[a-z][^>]*>$"
            last_data_find = re.sub(t_re_exp, "", string=last_data_find, count=1, flags=re.IGNORECASE)
            last_data_find = strip_useless_html_tag(last_data_find)
            # 保存数据
            res_data[last_data] = last_data_find
            last_data = "poutput"
        # print(last_data_find)
        # 找 Sample Input
        t_re_exp = "[\s|\S]*<[a-z][^>]*>\s*Sample\s+Input\s*</[a-z][^>]*>"
        # 提取数据
        t_data_find = re.compile(t_re_exp, flags=re.IGNORECASE).findall(prob_cont_body)
        if len(t_data_find) > 0:
            last_data_find = t_data_find[0]
            # 去除数据
            prob_cont_body = re.sub(t_re_exp, "", string=prob_cont_body, count=1, flags=re.IGNORECASE)
            # 处理数据
            t_re_exp = "<[a-z][^>]*>\s*Sample\s+Input\s*</[a-z][^>]*>$"
            last_data_find = re.sub(t_re_exp, "", string=last_data_find, count=1, flags=re.IGNORECASE)
            last_data_find = strip_useless_html_tag(last_data_find)
            # 保存数据
            res_data[last_data] = last_data_find
            last_data = "sample_input"
        # print(last_data_find)
        # 找 Sample Output
        t_re_exp = "[\s|\S]*<[a-z][^>]*>\s*Sample\s+Output\s*</[a-z][^>]*>"
        # 提取数据
        t_data_find = re.compile(t_re_exp, flags=re.IGNORECASE).findall(prob_cont_body)
        if len(t_data_find) > 0:
            last_data_find = t_data_find[0]
            # 去除数据
            prob_cont_body = re.sub(t_re_exp, "", string=prob_cont_body, count=1, flags=re.IGNORECASE)
            # 处理数据
            t_re_exp = "<[a-z][^>]*>\s*Sample\s+Output\s*</[a-z][^>]*>$"
            last_data_find = re.sub(t_re_exp, "", string=last_data_find, count=1, flags=re.IGNORECASE)
            last_data_find = strip_useless_html_tag(last_data_find)
            # 保存数据
            res_data[last_data] = last_data_find
            last_data = "sample_output"

        # 处理剩余数据
        res_data[last_data] = strip_useless_html_tag(prob_cont_body)
        # print(res_data[last_data])
        # t_re_exp = "<[a-z][^>]*>[\s(&nbsp;)]*$"
        # # print(re.compile(t_re_exp, flags=re.IGNORECASE).findall(last_data_find))
        # while len(re.compile(t_re_exp, flags=re.IGNORECASE).findall(last_data_find)) > 0:
        #     last_data_find = re.sub(t_re_exp, "", last_data_find, flags=re.IGNORECASE)
        # print(last_data_find)
        return res_data

    def get_status(self):
        # 得到Statistics页面URL
        status_url = self.soup.find('a',
                                    href=re.compile("Itemid=\d+&page=problem_stats&problemid=\d+&category=\d*",
                                                    flags=re.IGNORECASE))
        # 得到 题目数据完整 url
        status_url = urljoin(self.page_url, status_url['href'])
        # 下载网页
        html_content = str(downloader_from_url(status_url), encoding="utf-8")
        # 解析数据
        data_content = {
        }
        items_to_find = {
            "ac": "AC",
            "pe": "PE",
            "wa": "WA",
            "mle": "ML",
            "tle": "TL",
            "re": "RE",
            "ce": "CE",
            "se": "SE",
        }
        # 查找数据
        for key, value in items_to_find.items():
            t_find = re.compile(value + "\s*\(\d+\)").findall(html_content)
            if len(t_find) > 0:
                t_find = t_find[0].replace("(", "").replace(")", "").split()[-1]
                data_content[key] = t_find
        user_sub_info = re.compile("<td[^>]*>\d+</td>\s*<td[^>]*>\d+</td>\s*<td[^>]*>\d+</td>").findall(html_content)
        if len(user_sub_info) > 0:
            user_sub_info = user_sub_info[0]
            user_sub_info = re.findall(r'\d+', user_sub_info)
            data_content["total_sub"] = user_sub_info[0]
            data_content["user_sub"] = user_sub_info[1]
            data_content["user_ac"] = user_sub_info[2]
        return data_content
        pass


if __name__ == "__main__":
    # root_url = "https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8"
    # root_url = "https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8&category=617&page=show_problem&problem=4476"
    # root_url = "https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8&category=461&page=show_problem&problem=3608"
    # root_url = "https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8&category=617&page=show_problem&problem=4476"
    # root_url = "https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8&category=186&page=show_problem&problem=1264"
    # root_url = "https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8&page=problem_stats&problemid=201&category=5"
    root_url = "https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8&category=5&page=show_problem&problem=201"

    html_cont = downloader_from_url(root_url)
    parser = UVALiveHtmlParser(root_url, html_cont)
    print(parser.get_problem())
    pass
