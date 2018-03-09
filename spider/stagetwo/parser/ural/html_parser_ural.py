import re
from urllib.parse import urljoin
from spider.stagetwo.public.html_downloader import downloader_from_url
from spider.stagetwo.public.str_process import strip_useless_html_tag

from bs4 import BeautifulSoup, Tag, NavigableString
class UralHtmlPaser(object):
    def __init__(self,page_url, html_content):
        if page_url is None or str(page_url).strip() == "":
            raise Exception("UralHtmlParser: url不可为空")
        if html_content is None or str(html_content, encoding="utf-8").strip() == "":
            raise Exception("UralHtmlParser: 内容不可为空")

        self.page_url = page_url
        if page_url.find("problemset"):
            self.page_url = page_url.split("problemset")[0]
        self.html_content = html_content
        self.str_html_content = str(html_content)
        self.soup = BeautifulSoup(html_content, "html.parser", from_encoding="utf-8")
        if self.soup.find(text="Problem not found"):
            raise Exception("UralHtmlParser: 此题不存在")
        pass
    def get_urls(self):
        new_urls=set()
        links = self.soup.find_all('a', href=re.compile(r"(^problem.aspx\?space=1&num=\d+$)"))
        for tag in links:
            t_url = tag['href']
            t_url = urljoin(self.page_url, t_url)
            new_urls.add(t_url)
        return new_urls
        pass
    def get_problem(self):

        if self.page_url.find("problem.aspx?space=1&num=")<0:

            return None
        # 重置所有图片链接
        imgs = self.soup.find_all('img')
        # print(imgs)
        for img in imgs:
            img['src'] = urljoin(self.page_url, img['src'])

        imgs = self.soup.find_all('image')
        for img in imgs:
            # print(urljoin(page_url, img['src']))
            img['src'] = urljoin(self.page_url, img['src'])
        #题目内容
        res_data = {"url": self.page_url, "ojname": "Ural"}
        #id and title
        str1=self.soup.find('h2',class_="problem_title").text
        res_data["sourceid"]=re.findall(re.compile(r"\d+"),str1)[0]
        res_data["title"]=re.split(re.compile(r'\d+. '),str1)[1]
        #由于时间限制和内存限制在一个标签里，所以用正则将他们匹配出来
        try:
          limittag=self.soup.find('div',class_="problem_limits").get_text()

          ml=re.findall(re.compile(r'\d+'),limittag)[2]+'MB'
          tl=re.findall(re.compile(r'\d+.\d+'),limittag)[0]
          tl1=re.findall(re.compile(r'\d+'),tl)[0]
          tl2=re.findall(re.compile(r'\d+'),tl)[1]
          tml=''
          if int(tl2)==0:
            tml=tl1+'s'
          else:
            tml=tl1+'.'+tl2+'s'
          res_data["time_limit"]=tml
          res_data["memory_limit"]=ml
        except:
          res_data["time_limit"]=""
          res_data["memory_limit"]=""
        try:
          texts=self.soup.find('div',id="problem_text").contents
          text=""
          for i in texts:
            text=text+str(i)
          #print(text)
          text=strip_useless_html_tag(text)
          rep=re.compile(r"<h3 class=\"problem_subtitle\">Input</h3>")
          res_data["description"]=re.split(rep,text)[0]
          surplus=re.split(rep,text)[1]
          rep_input=re.compile(r"<h3 class=\"problem_subtitle\">Output</h3>")
          res_data["pinput"] = re.split(rep_input,surplus)[0]
          surplus_output=re.split(rep_input,surplus)[1]
          rep_output=re.compile(r"<h3 class=\"problem_subtitle\">Sample</h3>|<h3 class=\"problem_subtitle\">Samples</h3>")
          res_data["poutput"] = re.split(rep_output,surplus_output)[0]
        except:
            res_data["description"]=""
            res_data["pinput"] = ""
            res_data["poutput"] = ""
            pass
        try:
           sap=self.soup.find('table',class_="sample")
           saptrs=''
           if sap is not None:
            saptrs=sap.find_all('tr')
           sin=''
           sout=''
           for saptr in saptrs:
            saptds=saptr.find_all('td')
            haha=True
            for saptd in saptds:

                if haha is True:
                    sin=sin+saptd.text+"<br>"
                    haha=False
                else:
                    sout=sout+saptd.text+"<br>"
                    haha=True
            res_data["sample_input"]=sin
            res_data["sample_output"]=sout
        except:
            res_data["sample_input"]=""
            res_data["sample_output"]=""
        if self.soup.find(text='Notes')is not None:
              res_data["hint"]=self.soup.find(text='Notes').next.text
        else:
              res_data["hint"]=''
        if self.soup.find('div',class_="problem_source") is not  None:
              res_data["source"]=self.soup.find('div',class_="problem_source").text
        else:
              res_data["source"]=""
        #print(res_data["poutput"])
        return res_data








        #print(text)
        #print(res_data)
    def get_status(self):
        statistics = {}
        link_all = self.soup.find_all('a', href=re.compile(r"(^status.aspx\?space=1&num=\d+$)"))
        num_all=re.compile(r"\d+").findall(str(link_all))[2]
        num_ac=re.compile(r"\d+").findall(str(link_all[0].find_next('a')))[2]
        statistics["total_sub"]=num_all
        statistics["ac"]=num_ac
        statistics["ojname"]="Ural"
        statistics["sourceid"]=re.compile("\d+$").findall(self.page_url)[0]

        return statistics

        pass


if __name__=="__main__":
    uurl = "http://acm.timus.ru/problem.aspx?space=1&num=1387"
    html_cont = downloader_from_url(uurl)
    paser=UralHtmlPaser(uurl,html_cont)
    paser.get_problem()