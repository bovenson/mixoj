# codding: utf-8
from knowledge_tree.search.baidu_search import search_by_baidu as _search_by_baidu
from knowledge_tree.search.qihuso_search import search_by_qihuso as _search_by_qihuso
from knowledge_tree.search.sogou_search import search_by_sogou as _search_by_sogou
from knowledge_tree.search.bing_search import search_by_bing as _search_by_bing
import threading


def get_search_content(key_word):
    """给出关键字, 调取搜索函数(各个搜索引擎/博客/其他的搜索结果), 返回搜索结果集
    类型是字典, key是搜索引擎名/博客名/其他
    """
    # key_words = str(key_word).split()
    # key_word = "  +".join(key_words)
    # key_word = "+" + key_word
    # print(key_word)

    search_result = {}
    # 使用多线程
    threads = list()
    # 从百度获取结果的线程
    threads.append(threading.Thread(target=search_baidu, args=(key_word, search_result)))
    # 从360获取结果的线程
    threads.append(threading.Thread(target=search_qihuso, args=(key_word, search_result)))
    # # 从搜狗获取结果的线程
    # threads.append(threading.Thread(target=search_sogou, args=(key_word, search_result)))
    # 从bing获取结果的线程
    threads.append(threading.Thread(target=search_bing, args=(key_word, search_result)))

    for _thread in threads:
        # _thread.setDaemon(True)
        _thread.start()
    # 等待所有线程结束
    for _thread in threads:
        _thread.join()
    return search_result
    pass


def search_bing(key_word, _dict_search_result):
    # 从bing搜索获取结果
    try:
        _t_res = _search_by_bing(key_word=key_word)
        if _t_res is None:
            raise Exception("网络超时, 或搜索引擎页面升级导致分析失败")
        else:
            _dict_search_result["bing"] = _t_res
    except Exception as e:
        print("Bing搜索" + key_word + "时出错: ", e)


def search_sogou(key_word, _dict_search_result):
    # 从搜狗搜索获取结果
    try:
        _t_res = _search_by_sogou(key_word=key_word)
        if _t_res is None:
            raise Exception("网络超时, 或搜索引擎页面升级导致分析失败")
        else:
            _dict_search_result["sogou"] = _t_res
    except Exception as e:
        print("搜狗搜索" + key_word + "时出错: ", e)


def search_qihuso(key_word, _dict_search_result):
    # 从360搜索获取结果
    try:
        _t_res = _search_by_qihuso(key_word=key_word)
        if _t_res is None:
            raise Exception("网络超时, 或搜索引擎页面升级导致分析失败")
        else:
            _dict_search_result["qihuso"] = _t_res
    except Exception as e:
        print("360搜索搜索" + key_word + "时出错: ", e)


def search_baidu(key_word, _dict_search_result):
    # 从百度获取结果
    try:
        _t_res = _search_by_baidu(key_word=key_word)
        if _t_res is None:
            raise Exception("网络超时, 或搜索引擎页面升级导致分析失败")
        else:
            _dict_search_result["baidu"] = _t_res
    except Exception as e:
        print("百度搜索" + key_word + "时出错: ", e)
    pass
