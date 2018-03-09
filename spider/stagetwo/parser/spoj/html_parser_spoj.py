from bs4 import BeautifulSoup
import re
import os
import sys
from spider.stagetwo.public.html_downloader import downloader_from_url
from urllib.parse import urljoin
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '../..')))
if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mixoj.settings")
    django.setup()
from mixojapp.models import  SpojProblem
class SpojHtmlParser(object):
    def __init__(self, page_url, html_content):
        # 错误判断
        if page_url is None or str(page_url).strip() == "":
            raise Exception("SpojHtmlParser: url不可为空")
        if html_content is None or str(html_content, encoding="utf-8").strip() == "":
            raise Exception("SpojHtmlParser: 内容不可为空")
        self.page_url = page_url
        if page_url.find("/problems/classical"):
            self.page_url = page_url.split("/problems/classical")[0]
        self.html_content = html_content
        #转换成字符串格式
        self.str_html_content = str(html_content)
        self.soup = BeautifulSoup(html_content, "html.parser", from_encoding="utf-8")
        if self.soup.find(text="Not Found"):
            raise Exception("SpojHtmlParser: 此题不存在")
        pass
    def get_urls(self):
        new_urls = set()
        links = self.soup.find_all('a', href=re.compile(r"(^/problems/classical/sort=0,start=\d+$)"))

        for i in links:
            for tag in links:
               t_url = tag['href']
               t_url = urljoin(self.page_url, t_url)
               new_urls.add(t_url)
        try:
            table=self.soup.find('div',class_="table-responsive").find_next('table')
            trs=table.find('tbody').find_all('tr')
            for tr in trs:
                 problem={}
                 tds=tr.find_all('td')
                 p1=re.compile(r'\d+')
                 sourceid=re.findall(p1,tds[0].text)[0]
                 phref=tds[1].find('a')['href']
                 url='http://www.spoj.com'+phref+"/"
                 problem=SpojProblem(url=url,sourceid=sourceid)
                 problem.save()
                 new_urls.add(url)
        except:
            pass
        return new_urls
    def get_problem(self):
        if len(re.compile(r"http://www.spoj.com/problems/\w+/$").findall(self.page_url))==0:
            return  None
        imgs = self.soup.find_all('img')
        # print(imgs)
        for img in imgs:
            img['src'] = urljoin(self.page_url, img['src'])

        imgs = self.soup.find_all('image')
        for img in imgs:
            # print(urljoin(page_url, img['src']))
            img['src'] = urljoin(self.page_url, img['src'])
        res_data = {"url": self.page_url, "ojname": "Spoj"}
        try:
           title=self.soup.find('h2',id="problem-name").text
           res_data['title']=title
        except Exception as e:
            res_data['title']=''
        try:
            tlimit=self.soup.find(text="Time limit:").find_next('td').text
            res_data["time_limit"]=str(tlimit)
        except Exception as e:
            res_data["time_limit"]=''
        try:
            mlimit=self.soup.find(text="Memory limit:").next.text
            res_data['memory_limit']=mlimit
        except Exception as e:
            res_data['memory_limit']=""
        try:

            bb=str(self.soup.find('div',id="problem-body").contents)
            bodys=""
            for i in bb:
                bodys=bodys+str(i)
            des=""
            pinput=""
            poutput=""
            sample=""
            sample_input=""
            sample_output=""
            if self.soup.find(text="Input") is not None and self.soup.find(text="Output") is not None:

                if len(re.compile(r"<h3>Input</h3>").findall(bodys))>0:
                    des=des+re.split(re.compile(r"<h3>Input</h3>"),bodys)[0]
                    bodys=re.split(re.compile(r"<h3>Input</h3>"),bodys)[1]
                if len(re.compile(r"<h3>Output</h3>").findall(bodys))>0:
                    pinput=pinput+re.split(re.compile(r"<h3>Output</h3>"),bodys)[0]
                    bodys=re.split(re.compile(r"<h3>Output</h3>"),bodys)[1]
                if len(re.compile(r"<h3>Example</h3>").findall(bodys))>0:
                   poutput=poutput+re.split(re.compile(r"<h3>Example</h3>"),bodys)[0]
                   bodys=re.split(re.compile(r"<h3>Example</h3>"),bodys)[1]
            elif len(re.compile(r"<h3>Input</h3>").findall(bodys))==0 and len(re.compile(r"<h3>Output</h3>").findall(bodys))==0:

                if len(re.compile(r"<h3>Example</h3>").findall(bodys))>0:
                    des=des+re.split(re.compile(r"<h3>Example</h3>"),bodys)[0]
                else:
                    des=bodys
            elif len(re.compile(r"<h3>Input</h3>").findall(bodys))==0 and len(re.compile(r"<h3>Output</h3>").findall(bodys))>0:
                des=des+re.split(re.compile(r"<h3>Output</h3>"),bodys)[0]
                bodys=re.split(re.compile(r"<h3>Output</h3>"),bodys)[1]
                if len(re.compile(r"<h3>Example</h3>").findall(bodys))>0:
                   poutput=poutput+re.split(re.compile(r"<h3>Example</h3>"),bodys)[0]
                   bodys=re.split(re.compile(r"<h3>Example</h3>"),bodys)[1]
                else:
                   poutput=bodys
            elif len(re.compile(r"<h3>Input</h3>").findall(bodys))>0 and len(re.compile(r"<h3>Output</h3>").findall(bodys))==0:
                des=des+re.split(re.compile(r"<h3>Input</h3>"),bodys)[0]
                bodys=re.split(re.compile(r"<h3>Input</h3>"),bodys)[1]
                if len(re.compile(r"<h3>Example</h3>").findall(bodys))>0:
                   pinput=pinput+re.split(re.compile(r"<h3>Example</h3>"),bodys)[0]
                   bodys=re.split(re.compile(r"<h3>Example</h3>"),bodys)[1]
                else:
                   pinput=bodys
            elif len(re.compile(r"<h3>Input Specification</h3>").findall(bodys))>0 and len(re.compile(r"<h3>Output Specification</h3>").findall(bodys))>0:
                if len(re.compile(r"<h3>Input Specification</h3>").findall(bodys))>0:
                    des=des+re.split(re.compile(r"<h3>Input Specification</h3>"),bodys)[0]
                    bodys=re.split(re.compile(r"<h3>Input Specification</h3>"),bodys)[1]
                if len(re.compile(r"<h3>Output Specification</h3>").findall(bodys))>0:
                    pinput=pinput+re.split(re.compile(r"<h3>Output Specification</h3>"),bodys)[0]
                    bodys=re.split(re.compile(r"<h3>Output Specification</h3>"),bodys)[1]
                if len(re.compile(r"<h3>Example</h3>").findall(bodys))>0:
                   poutput=poutput+re.split(re.compile(r"<h3>Example</h3>"),bodys)[0]
                   bodys=re.split(re.compile(r"<h3>Example</h3>"),bodys)[1]
            elif len(re.compile(r"<h3>Input Specification</h3>").findall(bodys))==0 and len(re.compile(r"<h3>Output Specification</h3>").findall(bodys))==0:
                if len(re.compile(r"<h3>Example</h3>").findall(bodys))>0:
                    des=des+re.split(re.compile(r"<h3>Example</h3>"),bodys)[0]
                else:
                    des=bodys
            elif len(re.compile(r"<h3>Input Specification</h3>").findall(bodys))==0 and len(re.compile(r"<h3>Output Specification</h3>").findall(bodys))>0:
                des=des+re.split(re.compile(r"<h3>Output Specification</h3>"),bodys)[0]
                bodys=re.split(re.compile(r"<h3>Output Specification</h3>"),bodys)[1]
                if len(re.compile(r"<h3>Example</h3>").findall(bodys))>0:
                   poutput=poutput+re.split(re.compile(r"<h3>Example</h3>"),bodys)[0]
                   bodys=re.split(re.compile(r"<h3>Example</h3>"),bodys)[1]
                else:
                   poutput=bodys
            elif len(re.compile(r"<h3>Input Specification</h3>").findall(bodys))>0 and len(re.compile(r"<h3>Output Specification</h3>").findall(bodys))==0:
                des=des+re.split(re.compile(r"<h3>Input Specification</h3>"),bodys)[0]
                bodys=re.split(re.compile(r"<h3>Input Specification</h3>"),bodys)[1]
                if len(re.compile(r"<h3>Example</h3>").findall(bodys))>0:
                   pinput=pinput+re.split(re.compile(r"<h3>Example</h3>"),bodys)[0]
                   bodys=re.split(re.compile(r"<h3>Example</h3>"),bodys)[1]
                else:
                   pinput=bodys

            #print(pinput)

            #print(poutput)
            if self.soup.find(text="Example") is not None:
                a=self.soup.find(text="Example").find_next("pre")
                if a.find(text="Input:") is not None:
                    sample_input=sample_input+str(a.find(text="Input:").next)
                if a.find(text="Output:") is not None:
                    sample_output=sample_output+str(a.find(text="Output:").next)
                if a.find(text="Sample Input:") is not None:
                    sample_input=sample_input+str(a.find(text="Sample Input:").next)
                if a.find(text="Sample Output:") is not None:
                    sample_output=sample_output+str(a.find(text="Sample Output:").next)
                if a.find(text="Input:") is  None and a.find(text="Sample Input:") is  None:
                    sample=a.text
                    if len(re.compile(r"Input:").findall(sample))>0:
                       text1=re.split(re.compile(r"Input:"),sample)[1]
                       sample_input=sample_input+re.split(re.compile(r"Output:"),text1)[0]
                       sample_output=sample_output+re.split(re.compile(r"Output:"),text1)[1]
                    if len(re.compile(r"Sample input:").findall(sample))>0:
                       text1=re.split(re.compile(r"Sample input:"),sample)[1]
                       sample_input=sample_input+re.split(re.compile(r"Sample output:"),text1)[0]
                       sample_output=sample_output+re.split(re.compile(r"Sample output:"),text1)[1]
            res_data["description"]=des
            res_data["pinput"]=pinput
            res_data["poutput"]=poutput
            res_data["sample_input"]=sample_input
            res_data["sample_output"]=sample_output
            source=""
            if self.soup.find(text="Resource:") is not None:
                source=self.soup.find(text="Resource:").next.text
                if source=="-":
                    source=""
            res_data["source"]=source
            hint=""
            res_data["hint"]=hint



        except Exception as e:
            import traceback
            print(traceback.format_exc())
            print(e)
        try:

            problem_id=SpojProblem.objects.get(url=self.page_url)
            res_data["sourceid"]=problem_id.sourceid
            print(1)
        except:
            pass

        return res_data
    def get_status(self):
        if len(re.compile(r"http://www.spoj.com/problems/\w+/$").findall(self.page_url))==0:
            return  None
        heihei=re.split(re.compile(r"problems"),self.page_url)
        statistics_page_url=heihei[0]+"ranks"+heihei[1]

        try:
            statistics_html_content = downloader_from_url(statistics_page_url)
            if statistics_html_content is None:
                statistics_html_content = downloader_from_url(statistics_page_url)
            if statistics_html_content is None:
                statistics_html_content = downloader_from_url(statistics_page_url)
            statistics_soup = BeautifulSoup(statistics_html_content, "html.parser", from_encoding="utf-8")
            statistics={}
            user_ac=""
            total_sub=""
            ac=""
            wa=""
            ce=""
            ree=""
            tle=""
            try:
                statistics_tag=str(statistics_soup.find('table',class_="table problems").find_next('tbody'))
                statistics_tag_all=re.compile(r"\d+").findall(statistics_tag)
                user_ac=statistics_tag_all[0]
                total_sub=statistics_tag_all[1]
                ac=statistics_tag_all[2]
                wa=statistics_tag_all[3]
                ce=statistics_tag_all[4]
                ree=statistics_tag_all[5]
                tle=statistics_tag_all[6]
            except Exception as e:
                print(e)
            statistics["ojname"]="Spoj"
            statistics["user_ac"]=user_ac
            statistics["total_sub"]=total_sub
            statistics["ac"]=ac
            statistics["wa"]=wa
            statistics["ce"]=ce
            statistics["re"]=ree
            statistics["tle"]=tle
            print(statistics)
            return statistics
        except Exception as e:
            print(e)


if __name__ == "__main__":
        #uurl = "http://www.spoj.com/problems/classical/sort=0,start=50"
        uurl = "http://www.spoj.com/problems/CRYPTO4/"
        html_cont = downloader_from_url(uurl)
        paser=SpojHtmlParser(uurl,html_cont)
        paser.get_problem()