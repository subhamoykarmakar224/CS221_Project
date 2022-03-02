import multiprocessing
import os
import shutil


class IndexMerger:
    def __init__(self, logging):
        self.N_CLUSTERS = 3
        self.logging = logging
        self.clustered_index_url = os.path.join(
            '.', 'Indexer', 'iclusters')
        self.logging.info(
            f'Number of index clusters to be formed...{self.N_CLUSTERS}')

    def get_directories(self):
        url_tmp = os.path.join('.', 'Indexer', 'tmp')
        folders = [x[0] for x in os.walk(url_tmp)]
        folders.remove(os.path.join('.', 'Indexer', 'tmp'))
        self.logging.info(f'Got {len(folders)} small indexes.')
        return folders

    def create_cluster_index_folder(self, N):
        if not os.path.isdir(self.clustered_index_url):
            os.mkdir(self.clustered_index_url)

        for n in range(N):
            p = os.path.join(self.clustered_index_url, 'cluster-' + str(n))
            self.logging.info(f'Generating cluster folder...{str(p)}')
            if not os.path.isdir(p):
                os.mkdir(p)

    def _cleanup(self):
        if os.path.isdir(self.clustered_index_url):
            shutil.rmtree(self.clustered_index_url)

    def _worker(self, data, icluster):
        icluster_folder = os.path.join(
            self.clustered_index_url, 'cluster-' + str(icluster))
        
        if len(data) == 1:
            self.logging.info(f'Nothing to merge: Copying: {data[0]} and {icluster_folder}')
            print(f'Nothing to merge: Copying file from {data[0]} to {icluster_folder}')
            files_list = os.listdir(data[0])
            for f in files_list:
                shutil.copy2(os.path.join(data[0], f), icluster_folder)
            return
        
        file_list = dict()
        for d in data:
            file_list[d] = self.get_2prefix_file_list(d)
        
        file_list = list(file_list.items())
        for i in range(1, len(file_list)):
            file_url_1 = file_list[0][0]
            file_url_2 = file_list[i][0]
            file_data_1 = file_list[0][1]
            file_data_1 = list(file_data_1.union(file_list[i][1]))
            self.logging.info(f'Merging: {file_url_1} and {file_url_2}')
            print(f'Merging: {file_url_1} and {file_url_2}')
            for i in range(len(file_data_1)):
                if not os.path.isfile(os.path.join(icluster_folder, file_data_1[i])):
                    p1 = os.path.join(icluster_folder, file_data_1[i])
                else:
                    p1 = os.path.join(file_url_1, file_data_1[i])
                p2 = os.path.join(file_url_2, file_data_1[i])
                data1, data2 = '', ''
                if os.path.isfile(p1):
                    with open(p1, 'r', encoding='utf-8') as f:
                        data1 = f.read()
                if os.path.isfile(p2):
                    with open(p2, 'r', encoding='utf-8') as f:
                        data2 = f.read()
                
                data1 += '\n'
                data1 += data2
                with open(os.path.join(icluster_folder, file_data_1[i]), 'w', encoding='utf-8') as f:
                    f.write(data1)
                
    def get_2prefix_file_list(self, url):
        return set(os.listdir(url))

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
        self.create_cluster_index_folder(
            len(small_index_folders_cluster.keys()))
        self.logging.info(
            f'Starting creation of {len(small_index_folders_cluster.keys())} consolidated clusters...')

        url_to_file_list = list()
        for _, b in small_index_folders_cluster.items():
            url_to_file_list.append(b)

        # TODO :: fix :: TypeError: cannot pickle 'module' object
        # p = multiprocessing.Pool(len(url_to_file_list))
        # p.map(self._worker, url_to_file_list)

        # TODO :: Replace below with above Pool(...)
        for i in range(0, len(url_to_file_list)):
            self._worker(url_to_file_list[i], i)

        self.logging.info(
            f'Created {len(small_index_folders_cluster.keys())} consolidated clusters...DONE.')
