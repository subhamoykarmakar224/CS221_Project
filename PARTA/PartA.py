import ray
import Constants
import re, time


file_uri = './res/books/Ulysses_big.txt'
regex = r"\s"
token_word_count = dict()


def file_read_chunks():
    with open(file_uri, mode="r", encoding="utf-8-sig") as f:
        last_space, cnt, next_seek_start = 0, 0, 0
        left_out_str = ''
        while chunk := f.read(Constants.CHUNK_SIZE):
            last_space = chunk.rfind(' ')
            curr_chunk = left_out_str + chunk[:last_space]
            left_out_str = chunk[last_space:]
            my_tokenizer.remote(curr_chunk)

    print("---------------")
    for k in token_word_count:
        print(k, token_word_count[k])
    print("---------------")


@ray.remote
def my_tokenizer(s: str):
    res = re.split(regex, s.lower(), flags=re.I | re.M | re.MULTILINE)
    for r in res:
        if r not in token_word_count:
            token_word_count[r] = 0
        token_word_count[r] += 1


if __name__ == '__main__':
    start_time = time.time()
    file_read_chunks()
    print("Exec time --- %s seconds ---" % (time.time() - start_time))
