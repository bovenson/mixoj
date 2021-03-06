# coding: utf-8
from urllib.parse import quote
from knowledge_tree.downloader.html_downloader import HtmlDownloader
from bs4 import BeautifulSoup
from knowledge_tree.search.disturb_words import remove_disturb_words


def search_by_bing(key_word):
    res = None
    try:
        url = "http://cn.bing.com/search?q=" + quote(string=key_word, encoding="utf-8")
        # 下载结果
        search_result = HtmlDownloader.download(url)
        # bs 处理
        soup = BeautifulSoup(search_result, "html.parser")
        tags = soup.find('ol', id="b_results")
        res = ""
        for string in tags.stripped_strings:
            # print(string)
            res += string
        pass
    except:
        pass

    try:
        key_word += " 思路"
        url = "http://cn.bing.com/search?q=" + quote(string=key_word, encoding="utf-8")
        # print(url)
        # 下载结果
        search_result = HtmlDownloader.download(url)
        # bs 处理
        soup = BeautifulSoup(search_result, "html.parser")
        tags = soup.find('ol', id="b_results")
        res = ""
        for string in tags.stripped_strings:
            # print(string)
            res += string
        pass
    except:
        pass

    return remove_disturb_words(res)
    pass

if __name__ == "__main__":
    search_by_bing("poj 2162")
    pass
