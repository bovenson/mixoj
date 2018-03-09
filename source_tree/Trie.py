class TrieTree:
    tree = {}
    def __init__(self):
        self.tree.clear()
        pass

    def add(self, word, abb='none'):
        tree = self.tree
        for ch in word:
            if ch in tree:
                tree = tree[ch]
            else:
                tree[ch] = {}
                tree = tree[ch]
        tree['isEnd'] = True
        tree['abb'] = abb
        pass

    def find(self,word):
        tree = self.tree
        for ch in word:
            if ch in tree:
                tree = tree[ch]
            else:
                return False
        return 'isEnd' in tree
        pass

    def match(self,source):
        tree = self.tree
        cnt = len(source)
        ret = []
        for index in range(0,cnt):
            ch = source[index]
            if ch in tree:
                tree = tree[ch]
            else:
                break
            if 'isEnd' in tree and (index == cnt-1 or source[index+1] == ' '):
                if tree['abb'] == 'none':
                    ret.append(source[:index+1])
                else:
                    ret.append(tree['abb'])
        return ret
        pass

    def remove(self,word):
        tree = self.tree
        preNode = []
        for ch in word:
            preNode.append(tree)
            if ch in tree:
                tree = tree[ch]
            else:
                return
        if 'isEnd' in tree:
            del tree['isEnd']
            del tree['abb']
        while len(preNode) > 0:
            end_value = preNode[-1]
            if len(end_value) == 0 and 'isEnd' not in end_value:
                preNode.pop()
            else:
                break
        pass

if __name__ == '__main__':
    tree = TrieTree()
    pass