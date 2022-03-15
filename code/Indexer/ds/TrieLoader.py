import pickle
import os


class TrieNode:
    def __init__(self):
        self.children = dict()
        self.documents = list()


class TrieLoader:
    def __init__(self, url):
        self = self.load_root_trie_pickle(url)
        self.root = self.root

    def search_prefix(self, prefix):
        start_offset = 0
        end_offset = 0
        cur = self.root
        for c in prefix:
            if c not in cur.children:
                #break
                return (None, None)
            start_offset = cur.start_offset
            end_offset = cur.end_offset
            cur = cur.children[c]
        return (start_offset, end_offset)

    def load_root_trie_pickle(self, url):
        if not os.path.isfile(url):
            self.root = TrieNode()
            return self

        with open(url, 'rb') as f:
            pk = pickle.load(f)
            self.root = pk.root
        return pk
