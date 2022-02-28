import logging
import multiprocessing
import os
import shutil


class IndexMerger:
    def __init__(self, logging) -> None:
        self.N_CLUSTERS = 3
        self.logging = logging
        self.clustered_index_url = os.path.join(
            '.', 'Indexer', 'iclusters')
        self.logging.info(f'Number of index clusters to be formed...{self.N_CLUSTERS}')

    def get_directories(self):
        url_tmp = os.path.join('.', 'Indexer', 'tmp')
        folders = [x[0] for x in os.walk(url_tmp)]
        folders.remove(os.path.join('.', 'Indexer', 'tmp'))
        self.logging.info(f'Got {len(folders)} small indexes.')
        for i in range(len(folders)):
            f = folders[i]
            tmp = f.split('\\')[1:]
            folders[i] = tmp
        return folders

    def create_cluster_index_folder(self, N):
        if not os.path.isdir(self.clustered_index_url):
            os.mkdir(self.clustered_index_url)

        for n in range(N):
            p = os.path.join(self.clustered_index_url, 'cluster-' + str(n))
            logging.info(f'Generating cluster folder...{str(p)}')
            if not os.path.isdir(p):
                os.mkdir(p)

    def _cleanup(self):
        if os.path.isdir(self.clustered_index_url):
            shutil.rmtree(self.clustered_index_url)
    
    def _worker(self, data):
        print(data)

    def controller(self):
        self._cleanup()  # Clean clustered folder
        small_index_folders = self.get_directories()
        small_index_folders_cluster = dict()
        cnt = 0
        for i in range(0, len(small_index_folders), self.N_CLUSTERS):
            start = i
            end = i + self.N_CLUSTERS
            if end > len(small_index_folders):
                end = len(small_index_folders)
            small_index_folders_cluster[i] = small_index_folders[start:end]
            cnt += 1
        
        # Create the cluster folder
        self.create_cluster_index_folder(len(small_index_folders_cluster.keys()))
        self.logging.info(f'Starting creation of {len(small_index_folders_cluster.keys())} consolidated clusters...')

        url_to_file_list = list()
        for _, b in small_index_folders_cluster.items():
            url_to_file_list.append(b)
        
        # TODO :: fix :: TypeError: cannot pickle 'module' object
        # pool = multiprocessing.Pool(len(url_to_file_list))
        # pool.map(self._worker, url_to_file_list)

        # TODO :: Replace below with above Pool(...)        
        for f in url_to_file_list:
            self._worker(f)



        self.logging.info(f'Created {len(small_index_folders_cluster.keys())} consolidated clusters...DONE.')

