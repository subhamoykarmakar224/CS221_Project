from datetime import datetime
import multiprocessing
from datetime import datetime
import os
import shutil
import json
import io
from Indexer.Tokenizer import NLP
import logging

logging.basicConfig(
    filename='./logs/.log',
    format='%(levelname)s %(asctime)s :: %(message)s',
    level=logging.DEBUG
)
# Levels are as follows from most to least critical
#   CRITICAL
#   ERROR
#   WARNING
#   INFO
#   DEBUG


class IndexerController:
    def __init__(self, file_list):
        self.N_WORKERS = 4
        self.BATCH_SIZE = 300
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
        logging.info(f'Calculating... {i} => { i + len(file_list) - 1} , writing to: {folder_name}')

        # Create Sub-folders
        self.create_tmp_N_TMP_sub_folder(folder_name)

        for file_url in file_list:
            try:
                print(f'Parsing file...{file_url}')
                logging.info(f'Parsing file...{file_url}')
                with open(file_url, 'r') as f:
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
        res = self.tokenizer.word_tokenizer_count(content)
        for word, cnt_pos in res:
            word_count = cnt_pos[0]
            word_pos_list = cnt_pos[1]
            offset = self.index_cluster_fs(
                word,
                word_count,
                word_pos_list,
                folder_name,
                url
            )
            # self.index_of_index_tree(word, offset, folder_name)

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

        with open(os.path.join(folder_name, file_name), 'a') as f:
            offset = f.tell()
            s = [word, url, str(word_count), str(word_pos), '\n']
            s = '||'.join(s)
            f.write(s)

        return offset

    def index_of_index_tree(word, offset):
        pass

    def merge_indexes(self):
        logging.info('Merge index: Start')
        # TODO :: Merge intermediate indexes
        logging.info('Merge index: End')

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
        p = multiprocessing.Pool(self.N_WORKERS)
        p.map(self._worker, file_data.items())

        # TODO :: Merge Files
        self.merge_indexes()

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


# Start Indexer
if __name__ == '__main__':
    url_analyst = '../dataset/ANALYST/'
    url_dev = '../dataset/DEV/'
    clean_up_tmp()  # Clean up old indexed files
    file_list = get_list_of_files(url_analyst)  # Get list of files and URLs

    t1 = datetime.now()
    indexer = IndexerController(file_list)
    indexer.controller()
    t2 = datetime.now()

    print(f'Exec Time {t2 - t1}')
