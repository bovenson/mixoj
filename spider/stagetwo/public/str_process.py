# encoding: utf-8
import re


def _remove(re_exp, html_cont):
    flag = False
    # print(re_exp)
    # print(html_cont)
    if len(re.compile(re_exp, flags=re.IGNORECASE).findall(html_cont)) > 0:
        html_cont = re.sub(re_exp, "", string=html_cont, flags=re.IGNORECASE)
        flag = True
    # print(html_cont)
    return flag, html_cont
    pass


def strip_useless_html_tag(html_cont):
    """去除一段html代码前后端无用或错误的代码"""
    # 循环标记
    flag = True
    while flag:
        flag = False

        # 去除开头空白字符
        t_re_exp = "^\s"
        is_remove, html_cont = _remove(t_re_exp, html_cont)
        if is_remove is True:
            flag = True
            continue

        # 去除开头&nbsp;
        t_re_exp = "^&nbsp;"
        is_remove, html_cont = _remove(t_re_exp, html_cont)
        if is_remove is True:
            flag = True
            continue

        # 去除开头 html 关闭标签
        t_re_exp = "^</[a-z][^>]*>"
        is_remove, html_cont = _remove(t_re_exp, html_cont)
        if is_remove is True:
            flag = True
            continue

        # 去除开头 html 关闭标签
        t_re_exp = "^<[a-z][^>]*/>"
        is_remove, html_cont = _remove(t_re_exp, html_cont)
        if is_remove is True:
            flag = True
            continue

        # 去除开头空白标签
        t_re_exp = "^<[a-z][^>]*>(\s|(&nbsp;))*</[a-z][^>]*>"
        is_remove, html_cont = _remove(t_re_exp, html_cont)
        if is_remove is True:
            flag = True
            continue

        # 去除结尾空白字符
        t_re_exp = "\s$"
        is_remove, html_cont = _remove(t_re_exp, html_cont)
        if is_remove is True:
            flag = True
            continue

        # 去除结尾&nbsp;
        t_re_exp = "&nbsp;$"
        is_remove, html_cont = _remove(t_re_exp, html_cont)
        if is_remove is True:
            flag = True
            continue

        # 去除结尾 html 未关闭的标签
        t_re_exp = "<[a-z][^.>]*>$"
        is_remove, html_cont = _remove(t_re_exp, html_cont)
        if is_remove is True:
            flag = True
            continue

        # 去除结尾 html 关闭的标签
        t_re_exp = "<[a-z][^.>]*/>$"
        is_remove, html_cont = _remove(t_re_exp, html_cont)
        if is_remove is True:
            flag = True
            continue

        # 去除尾部空白标签
        t_re_exp = "<[a-z][^>]*>(\s|(&nbsp;))*</[a-z][^>]*>$"
        is_remove, html_cont = _remove(t_re_exp, html_cont)
        if is_remove is True:
            flag = True
            continue
        pass
    return html_cont
    pass


if __name__ == "__main__":
    print(strip_useless_html_tag('''
    <font size="4" color="#ff0000"/>
    <a href="baidu.com">&nbsp;\n&nbsp;</a></b> &nbsp; </h>  \n  \r&nbsp;   \n haha \n&nbsp;\n<b> &nbsp; <h>
    <a href="baidu.com">&nbsp;</a>
    <font size="4" color="#ff0000"/>
    <font size="4" color="#ff0000">
    '''))
    pass
