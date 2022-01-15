import os, sys, mmap, time
from multiprocessing import Pool
from FileRead import *
import time


class Controller:
    def __init__(self, file_uri):
        self.file_uri = file_uri

    def controller(self):
        self.read_file()

    def read_file(self):
        f = FileRead(self.file_uri)
        f.file_read_chunks()


if __name__ == '__main__':
    # TODO :: Uncomment argv before submit
    # file_name = sys.argv[1]
    # print(file_name)
    start_time = time.time()
    file_name = './resources/books/Ulysses.txt'
    t = Controller(file_name)
    t.controller()
    print("Exec time --- %s seconds ---" % (time.time() - start_time))

