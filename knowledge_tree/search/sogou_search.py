# coding: utf-8
from urllib.parse import quote
from knowledge_tree.downloader.html_downloader import HtmlDownloader
from bs4 import BeautifulSoup
from knowledge_tree.search.disturb_words import remove_disturb_words


def search_by_sogou(key_word):
    res = None
    try:
        url = "https://www.sogou.com/web?query=" + quote(string=key_word, encoding="utf-8")
        # 下载结果
        _html_content = HtmlDownloader.download(url)
        # bs 处理
        # print(_html_content)
        soup = BeautifulSoup(_html_content, "html.parser")
        tags = soup.find('div', class_="results")
        res = ""
        for string in tags.stripped_strings:
            res += string
        pass
    except:
        pass

    try:
        key_word += " 思路"
        url = "https://www.sogou.com/web?query=" + quote(string=key_word, encoding="utf-8")
        # 下载结果
        _html_content = HtmlDownloader.download(url)
        # bs 处理
        # print(_html_content)
        soup = BeautifulSoup(_html_content, "html.parser")
        tags = soup.find('div', class_="results")
        res = ""
        for string in tags.stripped_strings:
            res += string
        pass
    except:
        pass
    return remove_disturb_words(res)
    pass

if __name__ == "__main__":
    search_by_sogou("poj 2162")
    pass
