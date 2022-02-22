
class TrieNode:
    def __init__(self, prefix):
        self.prefix = prefix
        self.children = dict()
        self.documents = list()
