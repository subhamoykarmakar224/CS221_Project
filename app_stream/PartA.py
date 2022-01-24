import time
from app_stream.jobpool.JobStreamer import *
from app_stream.filehandle.FileRead import FileRead
from app_stream.tokenizer.Tokenizer import MyTokenizer
from app_stream.utils import Constants


class Controller:
    def __init__(self, file_uri):
        self.file_uri = file_uri
        self.file_read = FileRead(self.file_uri)
        self.my_tokenizer = MyTokenizer()

    def controller(self):
        self.start_job_executor()

    def start_job_executor(self):
        stream_processor_mthreads(
            self.file_read.file_read_chunks(),
            self.my_tokenizer.my_tokenizer,
            num_workers=max(multiprocessing.cpu_count() - 2, Constants.N_WORKERS)
        )


if __name__ == '__main__':
    # TODO :: Uncomment argv before submit
    # file_name = sys.argv[1]
    # print(file_name)
    start_time = time.time()
    file_name = './res/books/Ulysses_big.txt'
    t = Controller(file_name)
    t.controller()
    print("Exec time --- %s seconds ---" % (time.time() - start_time))
