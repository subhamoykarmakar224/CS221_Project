import os
from tracemalloc import start
from Indexer.ds.TrieLoader import TrieLoader

class GetData:
    def __init__(self):
        self.search_index = list()
        self.load_search_index_ioi()
        self.index_file_url = list()

    def get_list_of_index_clusters(self, path):
        l = []
        for root, _, files in os.walk(path):
            for file in files:
                l.append(os.path.join(root, file))
        return l

    def load_search_index_ioi(self):
        files = self.get_list_of_index_clusters(os.path.join('.', 'Indexer', 'ioi'))
        for f in files:
            trie_loader = TrieLoader(f)
            self.search_index.append(trie_loader)
        

    def get_data(self, prefix):
        prefix = prefix.lower()
        search_result = []
        prefix_2d = ''
        if len(prefix) >= 2:
            prefix_2d = prefix[:2]
        else:
            prefix_2d = prefix

        for i in range(len(self.search_index)):
            trie_loader = self.search_index[i]
            start_off, end_off = trie_loader.search_prefix(prefix)
            index_2d_url = os.path.join('.', 'Indexer', 'iclusters', 'cluster-' + str(i))
            if not os.path.isfile(os.path.join(index_2d_url, prefix_2d + '.txt')):
                continue
            tmp = []
            cnt = 0
            with open(os.path.join(index_2d_url, prefix_2d + '.txt'), 'r') as f:
                f.seek(start_off)
                while f.tell() <= end_off or cnt != 30:
                    ln  = f.readline()
                    if len(ln) == 0: break
                    tmp.append(f.readline())
                    cnt += 1
            search_result = search_result + tmp[:30]
        
        return search_result
