import re
from urllib.parse import urljoin
from spider.stagetwo.public.html_downloader import downloader_from_url
import spider.stagetwo.public.html_downloader
from spider.stagetwo.public.str_process import strip_useless_html_tag

from bs4 import BeautifulSoup, Tag, NavigableString
class HustHtmlParser(object):
    def __init__(self,page_url,html_content):
        # 错误判断
        if page_url is None or str(page_url).strip() == "":
            raise Exception("HustHtmlParser: url不可为空")
        if html_content is None or str(html_content, encoding="utf-8").strip() == "":
            raise Exception("HustHtmlParser: 内容不可为空")

        self.page_url = page_url
        if page_url.find("list"):
            self.page_url = page_url.split("list")[0]
        self.html_content = html_content
        #转换成字符串格式
        self.str_html_content = str(html_content)
        self.soup = BeautifulSoup(html_content, "html.parser", from_encoding="utf-8")
        if self.soup.find('div',class_="alert alert-danger"):
            raise Exception("HustHtmlParser: 此题不存在")
    def get_urls(self):
        new_urls=set()
        links = self.soup.find_all('a', href=re.compile(r"(^/problem/list/\d+$)|(^/problem/show/\d+$)"))
        for tag in links:
            t_url = tag['href']
            t_url = urljoin(self.page_url, t_url)
            new_urls.add(t_url)
        return new_urls
        pass
    def get_problem(self):
        if self.page_url.find("http://acm.hust.edu.cn/problem/show")<0:
            return None
        imgs = self.soup.find_all('img')
        # print(imgs)
        for img in imgs:
            img['src'] = urljoin(self.page_url, img['src'])

        imgs = self.soup.find_all('image')
        for img in imgs:
            # print(urljoin(page_url, img['src']))
            img['src'] = urljoin(self.page_url, img['src'])
        res_data = {"url": self.page_url, "ojname": "Hust"}
        res_data["sourceid"]=str(re.findall(re.compile(r"\d+"),self.page_url)[0])
        res_data['title']=str(re.split(re.compile(r'- '),self.soup.find('h1',class_="page-title").get_text())[1])
        res_data['time_limit']=str(self.soup.find('span',class_="label label-warning").get_text())
        res_data['memory_limit']=str(self.soup.find('span',class_="label label-danger").get_text())
        links=self.soup.find('dd',id="problem-desc").contents
        des=""
        for i in links:
            des=des+str(i)
        res_data["description"]=str(des)
        res_data["pinput"]=str(self.soup.find(text="Input").find_next('dd'))
        res_data["poutput"]=str(self.soup.find(text="Output").find_next('dd'))
        res_data["sample_input"]=str(self.soup.find(text="Sample Input").find_next('dd'))
        res_data["sample_output"]=str(self.soup.find(text="Sample Output").find_next('dd'))
        res_data["hint"]=str(self.soup.find(text="Hint").find_next('dd'))
        res_data["source"]=str(self.soup.find(text="Source").find_next('dd'))

        return res_data

        #print(res_data)

        pass
    def get_status(self):
        if self.page_url.find("http://acm.hust.edu.cn/problem/show")<0:
            return None
        pid=re.compile(r"\d+").findall(self.page_url)[0]
        statistics_page_url="http://acm.hust.edu.cn/problem/summary/"+str(pid)
        statistics_html_content = downloader_from_url(statistics_page_url)
        statistics_soup = BeautifulSoup(statistics_html_content, "html.parser", from_encoding="utf-8")
        statistics = {}
        statistics["ojname"]="Hust"
        statistics["sourceid"]=pid
        statistics["total_sub"]=statistics_soup.find(text="Total Submissions").next.text
        statistics["user_sub"]=statistics_soup.find(text="Submitted User").next.text
        statistics["user_ac"]=statistics_soup.find(text="Solved User").next.text
        statistics["ac"]=statistics_soup.find(text="Accepted").next.text
        statistics["pe"]=statistics_soup.find(text="Presentation Error").next.text
        statistics["wa"]=statistics_soup.find(text="Wrong Answer").next.text
        statistics["tle"]=statistics_soup.find(text="Time Limit Exceed").next.text
        statistics["mle"]=statistics_soup.find(text="Memory Limit Exceed").next.text
        statistics["ole"]=statistics_soup.find(text="Output Limit Exceed").next.text
        statistics["re"]=statistics_soup.find(text="Runtime Error").next.text
        statistics["ce"]=statistics_soup.find(text="Compile Error").next.text

        return statistics








        #print(statistics_page_url)
        pass
if __name__=="__main__":
    uurl = "http://acm.hust.edu.cn/problem/show/1568"
    html_cont = downloader_from_url(uurl)
    paser=HustHtmlParser(uurl,html_cont)
    paser.get_status()