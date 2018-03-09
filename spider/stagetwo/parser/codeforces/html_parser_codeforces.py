import re
from urllib.parse import urljoin
from spider.stagetwo.public.html_downloader import downloader_from_url
import spider.stagetwo.public.html_downloader
from spider.stagetwo.public.str_process import strip_useless_html_tag
from bs4 import BeautifulSoup, Tag, NavigableString
class CodeHtmlParser(object):
    def __init__(self,page_url,html_content):
        if page_url is None or str(page_url).strip() == "":
            raise Exception("CodeHtmlParser: url不可为空")
        if html_content is None or str(html_content, encoding="utf-8").strip() == "":
            raise Exception("CodeHtmlParser: 内容不可为空")
        self.page_url = page_url
        if page_url.find("problemset/page/"):
            self.page_url = page_url.split("problemset/page/")[0]
        self.html_content = html_content
        #转换成字符串格式
        self.str_html_content = str(html_content)
        self.soup = BeautifulSoup(html_content, "html.parser", from_encoding="utf-8")


    def get_urls(self):
        new_urls=set()
        links = self.soup.find_all('a', href=re.compile(r"(^/problemset/problem/\d+/\w+)|"
                                                        r"(^/problemset/page/\d+)"))
        for tag in links:
            t_url=tag["href"]
            r_url="http://codeforces.com"+str(t_url)
            try:
                 new_urls.remove(r_url)
                 new_urls.add(r_url)
            except:
                 new_urls.add(r_url)
        return new_urls
    def get_problem(self):
        if self.page_url.find("http://codeforces.com/problemset/problem")<0:
            return  None
        imgs = self.soup.find_all('img')
        # print(imgs)
        for img in imgs:
            img['src'] = urljoin(self.page_url, img['src'])

        imgs = self.soup.find_all('image')
        for img in imgs:
            # print(urljoin(page_url, img['src']))
            img['src'] = urljoin(self.page_url, img['src'])
        res_data = {"url": self.page_url, "ojname": "CodeForces"}
        title=self.soup.find('div',class_="title").text
        res_data["title"]=re.split(re.compile(r"\w\."),title)[1]
        res_data["time_limit"]=re.compile(r"\d+").findall(str(self.soup.find('div',class_="time-limit")))[0]+"s"
        res_data["memory_limit"]=re.compile(r"\d+").findall(str(self.soup.find('div',class_="memory-limit")))[0]+"MB"
        try:
            res_data["description"]=str(self.soup.find('div',class_="header").next_sibling)

        except:
            res_data["description"]=""
        res_data["pinput"]=""
        try:
            pinputs=self.soup.find('div',class_="input-specification").find_next('div').next_siblings
            for i in pinputs:
                res_data["pinput"]=res_data["pinput"]+str(i)

        except:
            pass
        res_data["poutput"]=""
        try:
            pinputs=self.soup.find('div',class_="output-specification").find_next('div').next_siblings
            for i in pinputs:
                res_data["poutput"]=res_data["poutput"]+str(i)

        except:
            pass
        res_data["sample_input"]=""
        res_data["sample_output"]=""
        try:
            samples=self.soup.find('div',class_="sample-test")
            sample_inputs=samples.find_all('div',class_="input")
            sample_outputs=samples.find_all('div',class_="output")
            for i in sample_inputs:
                res_data["sample_input"]=res_data["sample_input"]+str(i.find('pre'))+"<br>"
            for i in sample_outputs:
                res_data["sample_output"]=res_data["sample_output"]+str(i.find('pre'))+"<br>"
        except:
            pass
        res_data["hint"]=""
        try:
            hints=self.soup.find('div',class_="note").find_next('div').next_siblings
            for i in hints:
                res_data["hint"]=res_data["hint"]+str(i)
            pass
        except:
            pass
        try:
            res_data["source"]=self.soup.find('a',href=re.compile("/contest/\d+")).text
        except:
            res_data["source"]=""
            pass
        source_id=re.compile(r"\d+/\w").findall(self.page_url)[0]
        source_ids=re.split(re.compile(r"/"),source_id)
        res_data["sourceid"]=source_ids[0]+source_ids[1]
        return res_data
    def get_status(self):
        if self.page_url.find("http://codeforces.com/problemset/problem")<0:
            return  None
        s={}
        return s




if __name__=="__main__":
    uurl = "http://codeforces.com/problemset/problem/656/E"
    #uurl = "http://codeforces.com/problemset/page/1"
    html_cont = downloader_from_url(uurl)
    paser=CodeHtmlParser(uurl,html_cont)
    paser.get_problem()
