# coding: utf-8
from knowledge_tree.db.db_operations import get_knowledge_tree, get_name_by_id
from knowledge_tree.main.entry import start_search, get_result

if __name__ == "__main__":
    # 多题
    # for pid in range(2170, 2179):
    #     search_content = "poj " + str(pid)
    #     try:
    #         best_match = get_result(search_content)
    #         print("对", search_content, "分类结果:")
    #         print("best match-> parent name:", get_name_by_id(best_match['pid']), " name:", best_match['name'],
    #               "weight:", best_match["weight"])
    #         print("/n")
    #     except Exception as e:
    #         import traceback
    #         traceback.print_exc()
    #
    #         print("对 " + search_content + " 构建知识树时出错:", e)

    # 单题
    search_content = "poj 2195"
    try:
        best_match = get_result(search_content)
        print("对", search_content, "分类结果:")
        print("best match-> parent name:", get_name_by_id(best_match['pid']), " name:", best_match['name'], "weight:",
              best_match["weight"])
    except Exception as e:
        import traceback
        traceback.print_exc()

        print("对 " + search_content + " 构建知识树时出错:", e)
    pass
