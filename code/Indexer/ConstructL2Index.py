import multiprocessing
import os
from Indexer.ds.TrieController import TrieController


class ConstructL2Index:
    def __init__(self, logging):
        self.logging = logging
        self.ioi_folder_path = os.path.join('.', 'Indexer', 'ioi')

    def get_icluster_folder(self):
        return os.listdir(
            os.path.join('.', 'Indexer', 'iclusters')
        )

    def get_list_of_files(self, path):
        l = []
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".txt"):
                    l.append(os.path.join(root, file))
        return l

    def _worker(self, path):
        files = self.get_list_of_files(path)
        for f_path in files:
            lines = []
            with open(f_path, 'r', encoding='utf-8') as f:
                lines = f. readlines()

            for i in range(len(lines)):
                try:
                    tmp = lines[i].split('\t')
                    if len(tmp) >= 4:
                        tmp[2] = int(tmp[2])
                        lines[i] = tmp
                    else:
                        lines[i] = ['', '', 0, '', '']
                except:
                    self.logging.error(f'Error parsing: {tmp} :: {lines[i]}')
                    lines[i] = ['', '', 0, '', '']

            lines = sorted(lines, key=lambda x: (x[0]), reverse=False)  # Sort by prefix
            # lines = sorted(lines, key=lambda x: (x[2]), reverse=True)  # Sort by freq

            with open(f_path, 'w', encoding='utf-8') as f:
                for l in lines:
                    if l[2] != 0:
                        l[2] = str(l[2])
                        f.write('\t'.join(l))

    def sort_cluster_controller(self):
        clusters = [os.path.join('.', 'Indexer', 'iclusters', folder)
                    for folder in self.get_icluster_folder()]
        for c in clusters:
            self.logging.info(f'Parsing cluster: {c}')
            self._worker(c)

    def create_ioi_folder(self):
        if not os.path.isdir(self.ioi_folder_path):
            os.mkdir(self.ioi_folder_path)

    def create_ioi_controller(self):
        self.logging.info('<<<< ------------------------ Build Index of index: start ------------------------ >>>>')
        self.create_ioi_folder()
        cluster_folder_list = os.listdir(
            os.path.join('.', 'Indexer', 'iclusters')
        )
        tries = []
        for i in range(len(cluster_folder_list)):
            tries.append(TrieController(f'trie-cluster-{i+1}'))
        
        for i in range(len(cluster_folder_list)):
            cluster_url = cluster_folder_list[i]
            self._w_create_tree(cluster_url, tries[i])

        self.logging.info('<<<< ------------------------ Build Index of index: end ------------------------ >>>>')

    def _w_create_tree(self, cluster_url, trie: TrieController):
        self.logging.info(f'Building index of index for cluster: {cluster_url}')
        file_list = self.get_list_of_files(os.path.join(
            '.', 'Indexer', 'iclusters', cluster_url))
        for file in file_list:
            with open(file, 'r', encoding='utf-8') as f:
                next_seek = 0
                while True:
                    line = f.readline()
                    if len(line) > 1:
                        prefix = line[:line.index('\t')]
                        # self.logging.info(f'Done building index for cluster: {cluster_url}')
                        trie.insert(prefix, next_seek)
                    if not line:
                        break
                    next_seek = f.tell()
        self.logging.info(f'Done building index for cluster: {cluster_url}')
        self.logging.info(f'Saving Trie cluster...')
        trie.save_trie_pickle()
        self.logging.info(f'Done...Saved Trie cluster at {trie.pickle_name}')

