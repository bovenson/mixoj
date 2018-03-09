# coding: utf-8


class KnowledgeTreeNode(object):
    def __init__(self, cid, pid, name, synonym):
        self.id = cid
        self.pid = pid
        self.parent_pos = None
        if isinstance(name, str):
            self.name = name.strip()
        else:
            self.name = str(name).strip()
        self.synonym = synonym
        self.key_words = None

        # 需要清除的内容
        self.weight = 0
        self.processed = False

    def __str__(self):
        return self.name
    pass
