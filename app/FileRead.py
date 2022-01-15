import Constants as Constant
from Tokenizer import *
from multiprocessing import Pool


class FileRead:
    def __init__(self, file_uri):
        self.file_uri = file_uri
        self.buffer_size = Constant.BUFFER_SIZE
        self.pool = Pool()
        self.tokenizer = MyTokenizer()

    def file_read_chunks(self):
        with open(self.file_uri, mode="r", encoding="utf-8") as f:
            last_space, cnt, next_seek_start = 0, 0, 0
            left_out_str = ''
            while chunk := f.read(Constant.CHUNK_SIZE):
                last_space = chunk.rfind(' ')
                curr_chunk = left_out_str + chunk[:last_space]
                left_out_str = chunk[last_space:]
                # TODO :: Send for Tokenizer
                # print(curr_chunk)
                self.send_to_tokenizer(curr_chunk)
                # self.send_to_tokenizer_pool(curr_chunk)
                # TODO :: Delete bottom part of the code later
                cnt += 1
                if cnt == 3:
                    break
                print("------------")

        self.pool_cleanup()

    def send_to_tokenizer(self, s):
        self.tokenizer.my_tokenizer(s)

    def send_to_tokenizer_pool(self, s):
        print('s:: ', s)
        self.pool.apply(self.tokenizer.my_tokenizer, s)

    def pool_cleanup(self):
        self.pool.close()
        self.pool.join()

    def file_read_line_chunks(self):
        cnt = 0
        with open(self.file_uri) as f:
            while text := f.readline():
                print(text)
                cnt += 1
                if cnt == 4:
                    break

    def file_read_multi_ps(self):
        pass

"""
Symbol,Company Name,Security Name,Market Category,Test Issue,Financial Status,Round Lot Size
AAIT,iShares MSCI All Country Asia Information Technology Index Fund,iShares MSCI All Country Asia Information Technology Index Fund,G,N,N,100.0
AAL,"American Airlines Group, Inc.","American Airlines Group, Inc. - Common Stock",Q,N,N,100.0
AAME,Atlantic American Corporation,Atlantic American Corporation - Common Stock,G,N,N,100.0
"""
