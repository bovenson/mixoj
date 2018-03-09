from source_tree.build_source_tree import build_one_oj
OJ_LIST_SZK = ['poj', 'zoj', 'sgu', 'uvalive','ural','hust','hdu','hysbz','codeforces']
def build_oj_by_name(oj_name):
    build_one_oj(oj_name)
def build_all_oj():
    for i in OJ_LIST_SZK:
        build_one_oj(str(i))
if __name__=="__main__":
    build_all_oj()