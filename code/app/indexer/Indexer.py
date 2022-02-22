import os
import time
import json
from app.indexer.utils.DataCleaner import separate_data
from app.indexer.nlp.Tokenizer import NLP
from app.indexer.ds.TrieController import TrieController


class Indexer:
    def __init__(self):
        self.npl = NLP()
        self.t = TrieController()

    def get_list_of_files(self, url):
        file_list = []
        for path, subdirs, files in os.walk(url):
            for name in files:
                file_list.append(os.path.join(path, name))

        return file_list

    # 1988
    # 55393
    def start_indexing(self, url):
        ts = time.time()
        file_list = self.get_list_of_files(url)
        for i in range(0, len(file_list[:1000])):
            print(f'Indexing...{i} of {len(file_list)}')
            self.read_file_tokenize(file_list[i])

        print(f'Time Taken for {len(file_list)} files: {str(time.time() - ts)}')

    def read_file_tokenize(self, file_uri):
        with open(file_uri, 'r') as f:
            web_dict_data = json.load(f)
            url = web_dict_data['url']
            web_content = web_dict_data['content']
            encoding = web_dict_data['encoding']
            # Get cleaned data
            meta_content_type, meta_content_charset, meta_keywords, meta_authors, meta_others, text_data, links = \
                separate_data(web_content, url, encoding, self.npl)

            # Add to Trie DS
            self.add_data_to_trie(text_data, file_uri)
            # print(
            # meta_content_type,
            # meta_content_charset,
            # meta_keywords,
            # meta_authors,
            # meta_others,
            # text_data,
            # links)

            # Add URLS
            self.save_urls(url, links)

    def add_data_to_trie(self, data, uri):
        for k in data:
            self.t.insert(k, uri, int(data[k]))
        self.t.save_trie_pickle()

    def save_urls(self, url, links):
        with open('./pickle/data/urls_in_page.txt', 'a') as f:
            f.write(url + '\t' + str(links) + '\n')


if __name__ == '__main__':
    ind = Indexer()
    # url_analyst = '../../data/analyst/ANALYST/'
    # ind.start_indexing(url_analyst)
    url_dev = '../../data/developer/DEV/'
    ind.start_indexing(url_dev)
