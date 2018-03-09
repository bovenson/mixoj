# codding: utf-8
from urllib.parse import urljoin
import re
from bs4 import BeautifulSoup
from spider.stagetwo.public.html_downloader import downloader_from_url
from spider.stagetwo.public.str_process import strip_useless_html_tag


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
        pass

        # 得到新的待爬取的url

    def get_urls(self):
        if self.page_url.find("show_problem&problem=") >= 0:
            return {}
        new_urls = set()
        links = self.soup.find_all('a', href=re.compile(r"(option=com_onlinejudge&Itemid=\d+&category=\d*$)|"
                                                        r"(option=com_onlinejudge&Itemid=\d+&category=\d*&"
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
        res_data = {"url": self.page_url, "ojname": "UVA", "sourceid": re.compile("\d+$").findall(self.page_url)[0]}
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

        # print(cont_body)
        # -----------------------------------------------
        # Input and OUTPUT格式
        t_re_exp = "[\s|\S]*<[a-z][^>]*>Input\s*and\s*Output\s*</[a-z][^>]*>"
        data_find = re.compile(t_re_exp, flags=re.IGNORECASE).findall(prob_cont_body)
        # print("Input and Output"+str( len(data_find)))
        # --------------------------------------------------------------------------------------
        if len(data_find) > 0:
            last_data_find = data_find[0]
            # 去除数据
            prob_cont_body = re.sub(t_re_exp, "", string=prob_cont_body, count=1, flags=re.IGNORECASE)
            print(prob_cont_body)
            # 处理数据
            # t_re_exp = "<[a-z][^>]*>The\s*input\s*</[a-z][^>]*>$"
            t_re_exp = "<[a-z][^>]*>\s*Input</[a-z][^>]*>$"
            last_data_find = re.sub(t_re_exp, "", string=last_data_find, count=1, flags=re.IGNORECASE)
            # last_data_find = strip_useless_html_tag(last_data_find)
            # 保存数据
            res_data["description"] = last_data_find
            # 找 Sample Input
            t_re_exp = "[\s|\S]*<[a-z][^>]*>\s*Sample\s+Input</[a-z][^>]*>"
            # 提取数据
            t_data_find = re.compile(t_re_exp, flags=re.IGNORECASE).findall(prob_cont_body)
            if len(t_data_find) > 0:
                last_data_find = t_data_find[0]
                # 去除数据
                prob_cont_body = re.sub(t_re_exp, "", string=prob_cont_body, count=1, flags=re.IGNORECASE)
                # 处理数据
                t_re_exp = "<[a-z][^>]*>\s*Sample\s+Input</[a-z][^>]*>$"
                last_data_find = re.sub(t_re_exp, "", string=last_data_find, count=1, flags=re.IGNORECASE)
                # last_data_find = strip_useless_html_tag(last_data_find)
                # 保存数据
                res_data["output"] = last_data_find
                res_data["input"] = last_data_find
                # last_data = "sample_input"

                # 找 Sample Output
                t_re_exp = "[\s|\S]*<[a-z][^>]*>\s*Sample\s+Output\s*</[a-z][^>]*>"
                # 提取数据
                t_data_find = re.compile(t_re_exp, flags=re.IGNORECASE).findall(prob_cont_body)
                if len(t_data_find) > 0:
                    last_data_find = t_data_find[0]
                    # 去除数据
                    prob_cont_body = re.sub(t_re_exp, "", string=prob_cont_body, count=1, flags=re.IGNORECASE)
                    # 处理数据
                    t_re_exp = "<[a-z][^>]*>\s*Sample\s+Output</[a-z][^>]*>$"
                    last_data_find = re.sub(t_re_exp, "", string=last_data_find, count=1, flags=re.IGNORECASE)
                    # last_data_find = strip_useless_html_tag(last_data_find)
                    # 保存数据
                    res_data["Sample_Input"] = last_data_find
                    # last_data = "sample_output"]

                # 处理剩余数据
                # res_data[last_data] = strip_useless_html_tag(prob_cont_body)
                res_data["sample_output"] = prob_cont_body
                return res_data



            # ===================================================================

        # Input Specification格式
        t_re_exp = "[\s|\S]*<[a-z][^>]*>Input\s*Specification\s*</[a-z][^>]*>"
        # t_re_exp = "[\s|\S]*<[a-z][^>]*>\s*Input</[a-z][^>]*>"
        data_find = re.compile(t_re_exp, flags=re.IGNORECASE).findall(prob_cont_body)
        # print("Input Specification" + str(len(data_find)))
        # 判断是否读到Input
        # --------------------------------------------------------------------------------------
        if len(data_find) > 0:
            last_data_find = data_find[0]
            # 去除数据
            prob_cont_body = re.sub(t_re_exp, "", string=prob_cont_body, count=1, flags=re.IGNORECASE)
            print(prob_cont_body)
            # 处理数据
            # t_re_exp = "<[a-z][^>]*>\s*input\s*</[a-z][^>]*>$"
            t_re_exp = "<[a-z][^>]*>Input\s*Specification\s*</[a-z][^>]*>$"
            last_data_find = re.sub(t_re_exp, "", string=last_data_find, count=1, flags=re.IGNORECASE)
            last_data_find = strip_useless_html_tag(last_data_find)
            # 保存数据
            res_data["description"] = last_data_find
            # print("Description" + str(res_data["description"]))




            t_re_exp = "[\s|\S]*<[a-z][^>]*>Output\s*Specification\s*</[a-z][^>]*>"
            # t_re_exp = "[\s|\S]*<[a-z][^>]*>[\s|\S]*Output[\s|\S]*</[a-z][^>]*>"
            # 提取数据
            t_data_find = re.compile(t_re_exp, flags=re.IGNORECASE).findall(prob_cont_body)

            if len(t_data_find) > 0:
                last_data_find = t_data_find[0]
                # 去除数据
                prob_cont_body = re.sub(t_re_exp, "", string=prob_cont_body, count=1, flags=re.IGNORECASE)
                # 处理数据
                t_re_exp = "<[a-z][^>]*>Output\s*Specification\s*</[a-z][^>]*>$"
                last_data_find = re.sub(t_re_exp, "", string=last_data_find, count=1, flags=re.IGNORECASE)
                last_data_find = strip_useless_html_tag(last_data_find)
                # 保存数据
                res_data["input"] = last_data_find

        # 找到Input
        # Input格式
        # t_re_exp = "[\s|\S]*<[a-z][^>]*>\s*input\s*</[a-z][^>]*>"
        # <A NAME="SECTION0001001000000000000000">\nInput</A>
        t_re_exp = "[\s|\S]*<[a-z][^>]*>Input</[a-z][^>]*>"

        data_find = re.compile(t_re_exp, flags=re.IGNORECASE).findall(prob_cont_body)
        print("Input" + str(len(data_find)))
        if len(data_find) == 0:
            print(str(prob_cont_body))
        # 判断是否读到Input
        # --------------------------------------------------------------------------------------
        if len(data_find) > 0:
            last_data_find = data_find[0]
            # 去除数据
            prob_cont_body = re.sub(t_re_exp, "", string=prob_cont_body, count=1, flags=re.IGNORECASE)
            print(prob_cont_body)
            # 处理数据
            # t_re_exp = "<[a-z][^>]*>\s*input\s*</[a-z][^>]*>$"
            t_re_exp = "<[a-z][^>]*>\s*Input\s*</[a-z][^>]*>$"
            last_data_find = re.sub(t_re_exp, "", string=last_data_find, count=1, flags=re.IGNORECASE)
            last_data_find = strip_useless_html_tag(last_data_find)
            # 保存数据
            res_data["description"] = last_data_find
            # print("Description" + str(res_data["description"]))




            t_re_exp = "[\s|\S]*<[a-z][^>]*>\s*output</[a-z][^>]*>"
            # t_re_exp = "[\s|\S]*<[a-z][^>]*>[\s|\S]*Output[\s|\S]*</[a-z][^>]*>"
            # 提取数据
            t_data_find = re.compile(t_re_exp, flags=re.IGNORECASE).findall(prob_cont_body)

            if len(t_data_find) > 0:
                last_data_find = t_data_find[0]
                # 去除数据
                prob_cont_body = re.sub(t_re_exp, "", string=prob_cont_body, count=1, flags=re.IGNORECASE)
                # 处理数据
                t_re_exp = "<[a-z][^>]*>Output</[a-z][^>]*>$"
                last_data_find = re.sub(t_re_exp, "", string=last_data_find, count=1, flags=re.IGNORECASE)
                last_data_find = strip_useless_html_tag(last_data_find)
                # 保存数据
                res_data["input"] = last_data_find

        # 找到\nInput
        # Input格式
        # t_re_exp = "[\s|\S]*<[a-z][^>]*>\s*input\s*</[a-z][^>]*>"
        # <A NAME="SECTION0001001000000000000000">\nInput</A>
        t_re_exp = "[\s|\S]*<[a-z][^>]*>\nInput</[a-z][^>]*>"

        data_find = re.compile(t_re_exp, flags=re.IGNORECASE).findall(prob_cont_body)
        # print("input" + str(len(data_find)))
        # if len(data_find) == 0:
        #    print(str(prob_cont_body))
        # 判断是否读到Input
        # --------------------------------------------------------------------------------------
        if len(data_find) > 0:
            last_data_find = data_find[0]
            # 去除数据
            prob_cont_body = re.sub(t_re_exp, "", string=prob_cont_body, count=1, flags=re.IGNORECASE)
            print(prob_cont_body)
            # 处理数据
            # t_re_exp = "<[a-z][^>]*>\s*input\s*</[a-z][^>]*>$"
            t_re_exp = "<[a-z][^>]*>\nInput\s*</[a-z][^>]*>$"
            last_data_find = re.sub(t_re_exp, "", string=last_data_find, count=1, flags=re.IGNORECASE)
            last_data_find = strip_useless_html_tag(last_data_find)
            # 保存数据
            res_data["description"] = last_data_find
            # print("Description" + str(res_data["description"]))




            t_re_exp = "[\s|\S]*<[a-z][^>]*>]\nOutput</[a-z][^>]*>"
            # t_re_exp = "[\s|\S]*<[a-z][^>]*>[\s|\S]*Output[\s|\S]*</[a-z][^>]*>"
            # 提取数据
            t_data_find = re.compile(t_re_exp, flags=re.IGNORECASE).findall(prob_cont_body)

            if len(t_data_find) > 0:
                last_data_find = t_data_find[0]
                # 去除数据
                prob_cont_body = re.sub(t_re_exp, "", string=prob_cont_body, count=1, flags=re.IGNORECASE)
                # 处理数据
                t_re_exp = "<[a-z][^>]*>\nOutput</[a-z][^>]*>$"
                last_data_find = re.sub(t_re_exp, "", string=last_data_find, count=1, flags=re.IGNORECASE)
                last_data_find = strip_useless_html_tag(last_data_find)
                # 保存数据
                res_data["input"] = last_data_find

        # ==============================================================================================
        # The Input格式
        t_re_exp = "[\s|\S]*<[a-z][^>]*>The\s*input\s*</[a-z][^>]*>"
        data_find = re.compile(t_re_exp, flags=re.IGNORECASE).findall(prob_cont_body)
        # print("The Input" + str(len(data_find)))
        # --------------------------------------------------------------------------------------
        if len(data_find) > 0:
            last_data_find = data_find[0]
            # 去除数据
            prob_cont_body = re.sub(t_re_exp, "", string=prob_cont_body, count=1, flags=re.IGNORECASE)
            print(prob_cont_body)
            # 处理数据
            # t_re_exp = "<[a-z][^>]*>The\s*input\s*</[a-z][^>]*>$"
            t_re_exp = "<[a-z][^>]*>The\s*Input</[a-z][^>]*>$"
            last_data_find = re.sub(t_re_exp, "", string=last_data_find, count=1, flags=re.IGNORECASE)
            last_data_find = strip_useless_html_tag(last_data_find)
            # 保存数据
            res_data["description"] = last_data_find

            # The Output格式
            t_re_exp = "[\s|\S]*<[a-z][^>]*>The\s*output</[a-z][^>]*>"
            # t_re_exp = "[\s|\S]*<[a-z][^>]*>[\s|\S]*Output[\s|\S]*</[a-z][^>]*>"
            # 提取数据
            t_data_find = re.compile(t_re_exp, flags=re.IGNORECASE).findall(prob_cont_body)

            if len(t_data_find) > 0:
                last_data_find = t_data_find[0]
                # 去除数据
                prob_cont_body = re.sub(t_re_exp, "", string=prob_cont_body, count=1, flags=re.IGNORECASE)
                # 处理数据
                t_re_exp = "<[a-z][^>]*>the\s*Output</[a-z][^>]*>$"
                last_data_find = re.sub(t_re_exp, "", string=last_data_find, count=1, flags=re.IGNORECASE)
                last_data_find = strip_useless_html_tag(last_data_find)
                # 保存数据
                res_data["input"] = last_data_find

        # ============================================================








        # 找 Sample Input
        t_re_exp = "[\s|\S]*<[a-z][^>]*>\s*Sample\s+Input</[a-z][^>]*>"
        # 提取数据
        t_data_find = re.compile(t_re_exp, flags=re.IGNORECASE).findall(prob_cont_body)
        if len(t_data_find) > 0:
            last_data_find = t_data_find[0]
            # 去除数据
            prob_cont_body = re.sub(t_re_exp, "", string=prob_cont_body, count=1, flags=re.IGNORECASE)
            # 处理数据
            t_re_exp = "<[a-z][^>]*>\s*Sample\s+Input</[a-z][^>]*>$"
            last_data_find = re.sub(t_re_exp, "", string=last_data_find, count=1, flags=re.IGNORECASE)
            last_data_find = strip_useless_html_tag(last_data_find)
            # 保存数据
            res_data["output"] = last_data_find
            # last_data = "sample_input"

        # 找 Sample Output
        t_re_exp = "[\s|\S]*<[a-z][^>]*>\s*Sample\s+Output\s*</[a-z][^>]*>"
        # 提取数据
        t_data_find = re.compile(t_re_exp, flags=re.IGNORECASE).findall(prob_cont_body)
        if len(t_data_find) > 0:
            last_data_find = t_data_find[0]
            # 去除数据
            prob_cont_body = re.sub(t_re_exp, "", string=prob_cont_body, count=1, flags=re.IGNORECASE)
            # 处理数据
            t_re_exp = "<[a-z][^>]*>\s*Sample\s+Output</[a-z][^>]*>$"
            last_data_find = re.sub(t_re_exp, "", string=last_data_find, count=1, flags=re.IGNORECASE)
            last_data_find = strip_useless_html_tag(last_data_find)
            res_data["sample_input"] = last_data_find
            # last_data = "sample_output"]

        res_data["sample_output"] = prob_cont_body
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
    root_url = "https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=3&page=show_problem&problem=36"

    html_cont = downloader_from_url(root_url)
    parser = UVALiveHtmlParser(root_url, html_cont)
    print(parser.get_problem())
    pass
