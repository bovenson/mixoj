import re
from urllib.parse import urljoin
from spider.stagetwo.public.html_downloader import downloader_from_url
import spider.stagetwo.public.html_downloader
from spider.stagetwo.public.str_process import strip_useless_html_tag
from bs4 import BeautifulSoup, Tag, NavigableString
class HduHtmlParser(object):
    def __init__(self,page_url,html_content):
        if page_url is None or str(page_url).strip() == "":
            raise Exception("HduHtmlParser: url不可为空")
        if html_content is None or str(html_content, encoding="gb2312").strip() == "":
            raise Exception("HduHtmlParser: 内容不可为空")

        self.page_url = page_url
        if page_url.find("listproblem"):
            self.page_url = page_url.split("listproblem")[0]
        self.html_content = html_content
        #转换成字符串格式
        self.str_html_content = str(html_content)
        self.soup = BeautifulSoup(html_content, "html.parser", from_encoding="gb2312")
        if self.soup.find('strong'):
            raise Exception("HduHtmlParser: 此题不存在")
    def get_urls(self):
        new_urls=set()
        links = self.soup.find_all('a',href=re.compile(r"listproblem"))
        for tag in links:
             t_url = tag['href']
             t_url = urljoin(self.page_url, t_url)
             try:
                 new_urls.remove(t_url)
                 new_urls.add(t_url)
             except:
                 new_urls.add(t_url)
        scripts=self.soup.find('script',language="javascript")
        p=re.compile(r"\d+,\d+,-\d+")

        #p=re.compile(r"(\d+,\d+,-?\d+,^[\u4e00-\u9fa5_a-zA-Z0-9]+$,\d+,\d+)")
        strsoup=str(self.soup)
        ts=re.findall(p,strsoup)
        p2=re.compile(r",")
        for i in ts:
            pid=re.split(p2,i)[1]
            a_url="http://acm.hdu.edu.cn/showproblem.php?pid="+pid
            new_urls.add(a_url)

        return new_urls
    def get_problem(self):
        if self.page_url.find("http://acm.hdu.edu.cn/showproblem.php?pid=")<0:
            return  None
        imgs = self.soup.find_all('img')
        # print(imgs)
        for img in imgs:
            img['src'] = urljoin(self.page_url, img['src'])

        imgs = self.soup.find_all('image')
        for img in imgs:
            # print(urljoin(page_url, img['src']))
            img['src'] = urljoin(self.page_url, img['src'])
        res_data = {"url": self.page_url, "ojname": "Hdu"}
        res_data['title']=self.soup.find('table').contents[7].find_next('h1').text
        limitnode=self.soup.find('table').contents[7].find_next('font').text
        p6=re.compile(r'\d+')
        nums=re.findall(p6,limitnode)
        res_data['time_limit']=str(int(nums[1])/1000)+'s'
        res_data['memory_limit']=str(int(nums[3])/1024)+'MB'
        try:
            a=self.soup.find(text="Problem Description").find_next("div")
            res_data["description"]=str(a)
        except:
            res_data["description"]=""
        try:
            b=self.soup.find(text="Input").find_next("div")
            res_data["pinput"]=str(b)
        except:
            res_data["pinput"]=""
        try:
            d=self.soup.find(text="Output").find_next("div")
            res_data["poutput"]=str(d)
        except:
            res_data["poutput"]=""
        try:
            c=self.soup.find(text='Sample Input').find_next('div')
            res_data["sample_input"]=str(c)
        except:
            res_data["sample_input"]=""
        try:
            e=self.soup.find(text='Sample Output').find_next('div')
            res_data["sample_output"]=str(e)
        except:
            res_data["sample_output"]=""
        res_data["sourceid"]=re.compile(r"\d+").findall(self.page_url)[0]
        res_data["hint"]=""
        try:
            f=self.soup.find(text='Source').find_next('div')
            res_data["source"]=str(f)
        except:
            res_data["source"]=""
        return res_data
    def get_status(self):
        if self.page_url.find("http://acm.hdu.edu.cn/showproblem.php?pid=")<0:
            return  None
        pid=re.compile(r"\d+").findall(self.page_url)[0]
        statistics_page_url="http://acm.hdu.edu.cn/statistic.php?pid="+str(pid)
        statistics_html_content = downloader_from_url(statistics_page_url)
        statistics_soup = BeautifulSoup(statistics_html_content, "html.parser", from_encoding="gb2312")
        statistics={}
        statistics["ojname"]="Hdu"
        statistics["sourceid"]=pid
        statistics["total_sub"]=statistics_soup.find(text="Total Submission(s)").find_next('font').text
        statistics["user_ac"]=statistics_soup.find(text="User Accepted").find_next('font').text
        statistics["ac"]=statistics_soup.find(text="Accepted").find_next('font').text
        statistics["pe"]=statistics_soup.find(text="Presentation Error").find_next('font').text
        statistics["wa"]=statistics_soup.find(text="Wrong Answer").find_next('font').text
        statistics["re"]=statistics_soup.find(text="Runtime Error").find_next('font').text
        statistics["ce"]=statistics_soup.find(text="Compilation Error").find_next('font').text
        statistics["tle"]=statistics_soup.find(text="Time Limit Exceeded").find_next('font').text
        statistics["mle"]=statistics_soup.find(text="Memory Limit Exceeded").find_next('font').text
        statistics["ole"]=statistics_soup.find(text="Output Limit Exceeded").find_next('font').text
        statistics["se"]=statistics_soup.find(text="System Error").find_next('font').text
        return statistics







if __name__=="__main__":
    uurl = "http://acm.hdu.edu.cn/listproblem.php?vol=1"
    #uurl = "http://acm.hdu.edu.cn/showproblem.php?pid=3687"
    html_cont = downloader_from_url(uurl)
    paser=HduHtmlParser(uurl,html_cont)
    paser.get_urls()



