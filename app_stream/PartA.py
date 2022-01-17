import multiprocessing
import time
from app_stream.filehandle import *
from app_stream.jobpool import JobStreamer
from utils import Constants


class Controller:
    def __init__(self, file_uri):
        self.file_uri = file_uri
        self.file_read = FileRead(self.file_uri)
        self.job_pool_control = JobStreamer()

    def controller(self):
        self.read_file()

    def read_file(self):
        self.job_pool_control.stream_processor_mprocessor(
            self.file_read.file_read_chunks(),
            self.job_pool_control.stream_processor_mprocessor,
            num_workers=max(multiprocessing.cpu_count(), Constants.N_WORKERS)
        )


if __name__ == '__main__':
    # TODO :: Uncomment argv before submit
    # file_name = sys.argv[1]
    # print(file_name)
    start_time = time.time()
    file_name = './res/books/Ulysses.txt'
    t = Controller(file_name)
    t.controller()
    print("Exec time --- %s seconds ---" % (time.time() - start_time))
