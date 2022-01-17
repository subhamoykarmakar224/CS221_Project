from app_stream.utils import Constants


class FileRead:
    def __init__(self, file_uri):
        self.file_uri = file_uri

    def file_read_chunks(self):
        with open(self.file_uri, mode="r", encoding="utf-8-sig") as f:
            last_space, cnt, next_seek_start = 0, 0, 0
            left_out_str = ''
            while chunk := f.read(Constants.CHUNK_SIZE):
                last_space = chunk.rfind(' ')
                curr_chunk = left_out_str + chunk[:last_space]
                left_out_str = chunk[last_space:]
                # TODO :: Delete bottom part of the code later
                # cnt += 1
                # if cnt == 5:
                #     break
                yield curr_chunk
