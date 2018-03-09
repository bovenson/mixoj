# coding: utf-8
# 字符串的一些操作
import re


def str_is_equal_ignore_case(str1, str2):
    """不区分大小写判断两个变量字符串形式是否相同"""
    return str(str1).lower() == str(str2).lower()


def get_keywords(_synonym):
    return re.split('[,，]', _synonym)
    pass

if __name__ == "__main__":
    print(get_keywords("a,b c:sd，萨达"))
    # print(str_is_equal_ignore_case(None, None))
    pass
