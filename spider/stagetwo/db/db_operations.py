# codding: utf-8
# 使用 Django 模型实现数据存储
import os
import sys
# 如果没有设置 DJANGO_SETTINGS_MODULE, 则设置
if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    import django
    pathname = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, pathname)
    sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mixoj.settings")
    django.setup()
from mixojapp.models import Problem


def get_old_urls(oj_name):
    # 对 OJ 名判断
    if oj_name is None or str(oj_name) == "":
        return None
    que_res = Problem.objects.filter(ojname__iexact=oj_name).values('url')
    urls = []
    for url in que_res:
        urls.append(url.get('url'))
    return urls
    pass


if __name__ == "__main__":
    print(get_old_urls("Poj"))
    pass
