# coding: utf-8


# 在这里填写有可能产生干扰的词语, 如美图, 图片
disturb_words = [
    # 图
    "美图", "图片", "高清图", "大图", "地图",
    # 树
    "树上", "大树", "上树",
]


def remove_disturb_words(_search_result):
    if _search_result is None:
        return None
    if isinstance(_search_result, str) and _search_result.strip() == "":
        return None
    # 去除有可能影响结果的词语
    for _word in disturb_words:
        _search_result = _search_result.replace(_word, "")
    return _search_result
    pass
