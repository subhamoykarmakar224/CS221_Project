import logging
import os
import shutil


class IndexMerger:
    def __init__(self, logging, N_WORKERS) -> None:
        self.N_CLUSTERS = 4
        self.logging = logging
        self.N_WORKERS = N_WORKERS
        self.clustered_index_url = os.path.join(
            '.', 'Indexer', 'iclusters')
        self.logging.info(f'Number of index clusters to be formed...{self.N_CLUSTERS}')

    def get_directories(self):
        url_tmp = os.path.join('.', 'Indexer', 'tmp')
        folders = [x[0] for x in os.walk(url_tmp)]
        folders.remove(os.path.join('.', 'Indexer', 'tmp'))
        self.logging.info(f'Got {len(folders)} small indexes.')
        return folders

    def create_cluster_index_folder(self):
        if not os.path.isdir(self.clustered_index_url):
            os.mkdir(self.clustered_index_url)

        for n in range(self.N_CLUSTERS):
            p = os.path.join(self.clustered_index_url, 'cluster-' + str(n))
            logging.info(f'Generating cluster folder...{str(p)}')
            if not os.path.isdir(p):
                os.mkdir(p)

    def _cleanup(self):
        if os.path.isdir(self.clustered_index_url):
            shutil.rmtree(self.clustered_index_url)

    def controller(self):
        self._cleanup()  # Clean clustered folder
        self.create_cluster_index_folder()  # Create the cluster folder
        small_index_folders = self.get_directories()
        small_index_folders_cluster = dict()
        for i in range(0, len(small_index_folders), self.N_CLUSTERS):
            start = i
            end = i + self.N_CLUSTERS
            if end > len(small_index_folders):
                end = len(small_index_folders)
            small_index_folders_cluster[i] = small_index_folders[start:end]
        
        for k in small_index_folders_cluster:
            print(k, small_index_folders_cluster[k])
