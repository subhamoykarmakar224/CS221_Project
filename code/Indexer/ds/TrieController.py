import pickle, os


class TrieNode:
    def __init__(self):
        self.children = dict()
        self.documents = list()


class TrieController:
    def __init__(self):
        self = self.load_root_trie_pickle()
        self.root = self.root

    def insert(self, word, doc, cnt, url):
        cur = self.root
        depth = -1
        for c in word:
            depth += 1
            if c not in cur.children:
                cur.children[c] = TrieNode()

            if not cur.documents.__contains__((doc, cnt, url)):
                cur.documents.append((doc, cnt, url))

            if depth == 5:
                break

            cur = cur.children[c]

    def search_prefix(self, prefix):
        cur = self.root
        docs = []
        for c in prefix:
            if c not in cur.children:
                break
            docs = cur.documents
            cur = cur.children[c]
        return docs

    def load_root_trie_pickle(self):
        url = './app/indexer/pickle/data/root.pickle'
        # url = './pickle/data/root.pickle'

        if not os.path.isfile(url):
            self.root = TrieNode()
            return self

        with open(url, 'rb') as f:
            pk = pickle.load(f)
            self.root = pk.root

        return pk

    def save_trie_pickle(self):
        # url = './pickle/data/root.pickle'
        url = 'app/indexer/pickle/data/root.pickle'
        pk = self
        with open(url, 'wb') as f:
            pickle.dump(pk, f)

# if __name__ == '__main__':
#     s = ['apple', 'mouse', 'app', 'mousepad']
#     document = ['d1', 'd1', 'd2', 'd1']
#     cnt = [5, 7, 9, 10]
#     t = TrieController()
#     for i in range(len(s)):
#         t.insert(s[i], document[i], cnt[i], )
#     t.save_trie_pickle()

# print(t.search_prefix('mousep'))