# coding: utf-8
from urllib.parse import quote

import re

from knowledge_tree.downloader.html_downloader import HtmlDownloader
from bs4 import BeautifulSoup
from knowledge_tree.search.disturb_words import remove_disturb_words


def search_by_baidu(key_word):
    """"给出关键字,返回百度搜索结果"""
    _res = ""
    try:
        url = "http://www.baidu.com/s?wd=" + quote(string=key_word, encoding="utf-8")
        # 下载结果
        search_result = HtmlDownloader.download(url)
        # bs 处理
        soup = BeautifulSoup(search_result, "html.parser")
        tags = soup.find('div', id="content_left")
        for string in tags.stripped_strings:
            # print(string)
            _res += string
        pass
    except:
        pass

    try:
        key_word += " 思路"
        url = "http://www.baidu.com/s?wd=" + quote(string=key_word, encoding="utf-8")
        # print(url)
        # 下载结果
        search_result = HtmlDownloader.download(url)
        # bs 处理
        soup = BeautifulSoup(search_result, "html.parser")
        tags = soup.find('div', id="content_left")
        for tag in tags.children:
            # print(tag.text)
            _res += tag.text
        pass
    except:
        pass

    return remove_disturb_words(_res)
    pass


if __name__ == "__main__":
    # key_word = "poj 2165"
    # res = search_by_baidu(key_word)
    # print(len(re.findall("DFs", res, flags=re.IGNORECASE)))
    pass

#
# def deal(_res, _key_words):
#     _best_match = "未找到分类"
#     max_match = 0
#     for _key_word in _key_words:
#         cnt = 0
#         if isinstance(_key_word, str):
#             cnt = len(re.findall(_key_word, _res, flags=True))
#             if cnt > max_match:
#                 _best_match = _key_word
#         elif isinstance(_key_word, tuple):
#             for item in _key_word:
#                 cnt += len(re.findall(item, _res, flags=True))
#             if cnt > max_match:
#                 _best_match = _key_word[0]
#         pass
#     return _best_match
#     pass
#
#
# if __name__ == "__main__":
#     key_words = ["模拟", "二分", "回溯", ("动规", "动态规划"), "二叉树", "最短路", ("大数", "大整数")]
#     for pid in range(2100, 2199):
#         search_content = "poj " + str(pid)
#         try:
#             res = search_by_baidu(search_content)
#             best_match = deal(res, key_words)
#             pass
#         except TimeoutError:
#             print(search_content, ": ", "网络超时")
#             pass
#         except Exception as e:
#             print(search_content, ": ", e)
#             pass
#         else:
#             print(search_content, ": ", best_match)
#     # out_put = commands.getoutput("ls -la")
#     pass
#
