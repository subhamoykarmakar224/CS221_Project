
file_uri = './res/books/Ulysses.txt'
file_out = './res/books/Ulysses_big.txt'


def generate():
    f = open(file_out, 'a')
    for _ in range(220):
        with open(file_uri, 'r') as fs:
            f.write(str(fs.read()))
            f.write('\n')
    f.close()


if __name__ == '__main__':
    generate()
