import pickle
import os


class TrieNode:
    def __init__(self):
        self.children = dict()
        self.start_offset = -1
        self.end_offset = -1


class TrieController:
    def __init__(self, pickle_name):
        self.root = TrieNode()
        self.pickle_name = pickle_name

    def insert(self, word, offset):
        cur = self.root
        depth = -1
        for c in word:
            depth += 1
            if c not in cur.children:
                cur.children[c] = TrieNode()
                cur.start_offset = offset
                cur.end_offset = offset
            if c == word[-1]:
                cur.end_offset = max(cur.end_offset, offset)

            if depth == 10:
                break

            cur = cur.children[c]

    def search_prefix(self, prefix):
        cur = self.root
        for c in prefix:
            if c not in cur.children:
                break
            start_offset = cur.start_offset
            end_offset = cur.end_offset
            cur = cur.children[c]
        return (start_offset, end_offset)

    def save_trie_pickle(self):
        url = os.path.join('.', 'Indexer', 'ioi', self.pickle_name)
        pk = self
        with open(url, 'wb') as f:
            pickle.dump(pk, f)
