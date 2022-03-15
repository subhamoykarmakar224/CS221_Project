from dataclasses import asdict
from datetime import datetime
import multiprocessing
from datetime import datetime
import os
import shutil
import json
from Indexer.Tokenizer import NLP
from Indexer.IndexMerger import IndexMerger
from Indexer.ConstructL2Index import ConstructL2Index
import logging
from bs4 import BeautifulSoup


logging.basicConfig(
    filename='./logs/indexer.log',
    format='%(levelname)s %(asctime)s :: %(message)s',
    level=logging.DEBUG
)


class IndexerController:
    def __init__(self, file_list):
        self.N_WORKERS = 6
        self.BATCH_SIZE = 1000
        # self.N_WORKERS = 4
        # self.BATCH_SIZE = 400
        self.file_list = file_list
        self.tmp_folders = list()
        self.TMP_URL = os.path.join('.', 'Indexer', 'tmp')
        self.tokenizer = NLP()

    def _worker(self, data):
        i, file_list = data
        folder_name = os.path.join(self.TMP_URL, 'tmp' + str(i))
        print(
            f'Calculating... {i} => { i + len(file_list) - 1} , writing to: {folder_name}'
        )
        logging.info(
            f'Calculating... {i} => { i + len(file_list) - 1} , writing to: {folder_name}')

        # Create Sub-folders
        self.create_tmp_N_TMP_sub_folder(folder_name)

        for file_url in file_list:
            try:
                # print(f'Parsing file...{file_url}')
                logging.info(f'Parsing file...{file_url}')
                with open(file_url, 'r', encoding='utf-8') as f:
                    web_dict_data = json.load(f)
                    url = web_dict_data['url']
                    web_content = web_dict_data['content']
                    encoding = web_dict_data['encoding']
                    self.tokenize_and_get_posting_obj_list(
                        url, web_content, encoding, folder_name
                    )
            except:
                print(f'Error parsing...{file_url}')
                logging.error(f'Error parsing...{file_url}')

    def tokenize_and_get_posting_obj_list(self, url, content, encoding, folder_name):
        # Tuple(...('contact', [2, [3633, 3866]])...)
        soup = BeautifulSoup(str(content), 'html.parser')
        res = self.tokenizer.word_tokenizer_count(soup.text)
        for word, cnt_pos in res:
            word_count = cnt_pos[0]
            word_pos_list = cnt_pos[1]
            self.index_cluster_fs(
                word,
                word_count,
                word_pos_list,
                folder_name,
                url
            )

    def index_cluster_fs(self, word, word_count, word_pos, folder_name, url):
        offset = 0
        file_uri = ""
        if len(word) > 2:
            file_uri = word[:2]
        else:
            file_uri = word

        if not str(file_uri).isalpha():
            file_uri = 'special'

        file_name = file_uri + '.txt'

        with open(os.path.join(folder_name, file_name), 'a', encoding="utf-8") as f:
            s = [word, url, str(word_count), str(word_pos), '\n']
            s = '\t'.join(s)
            f.write(s)

    def create_tmp_N_TMP_folders(self):
        if not os.path.isdir(self.TMP_URL):
            os.mkdir(self.TMP_URL)

    def create_tmp_N_TMP_sub_folder(self, folder_name):
        os.mkdir(folder_name)

    def controller(self):
        logging.info(f'Number of concurrent workers: {self.N_WORKERS}')
        logging.info(f'Batch size: {self.BATCH_SIZE} files.')
        self.create_tmp_N_TMP_folders()
        file_data = dict()
        for i in range(0, len(self.file_list), self.BATCH_SIZE):
            start = i
            end = i + self.BATCH_SIZE
            if end > len(self.file_list):
                end = len(self.file_list)
            file_data[i] = self.file_list[start:end]

        # Start Parallel processing
        pool = multiprocessing.Pool(processes=self.N_WORKERS)
        pool.map(self._worker, file_data.items())
        
        # TODO :: Delete this later: for testing purpose only
        # self._worker((0, file_data[0]))

        logging.info('Success. All indexes created.')


def get_list_of_files(path):
    file_list = []
    for path, _, files in os.walk(path):
        for name in files:
            file_list.append(os.path.join(path, name))

    return file_list


def clean_up_tmp():
    TMP_URL = os.path.join('.', 'Indexer', 'tmp')
    if os.path.isdir(TMP_URL):
        shutil.rmtree(TMP_URL)


def clean_up_iclusters():
    TMP_URL = os.path.join('.', 'Indexer', 'iclusters')
    if os.path.isdir(TMP_URL):
        shutil.rmtree(TMP_URL)


def clean_up_ioi():
    TMP_URL = os.path.join('.', 'Indexer', 'ioi')
    if os.path.isdir(TMP_URL):
        shutil.rmtree(TMP_URL)


# Start Indexer
if __name__ == '__main__':
    url_analyst = '../dataset/ANALYST/'
    url_dev = '../DEV/'

    #START: STAGE 1: Build initial index
    # Clean up old indexed files
    # clean_up_tmp()
    # clean_up_iclusters()
    # clean_up_ioi()
    
    #Get list of files and URLs
    # file_list = get_list_of_files(url_dev)
    # print(f'Found {len(file_list)} files to index')
    # logging.info(f'Found {len(file_list)} files to index')

    # Create Index to form 3 clusters
    # indexer = IndexerController(file_list)
    # indexer.controller()
    #END: STAGE 1: Build initial index

    # START: STAGE 2: Build index of index
    # Merge Index to form 3 clusters
    # m = IndexMerger(logging)
    # m.controller()

    iofi = ConstructL2Index(logging)
    iofi.sort_cluster_controller()
    iofi.create_ioi_controller()
    # END: STAGE 2: Build index of index

    print(f'Done.')
