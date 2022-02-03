import os, re, sys
import Constants
import string


complete_token_count_list = list()

# ------------------ MAIN FUNCTIONS ------------------ #
"""
Tokenizes the string by reading the file in chunks and feeding the file to our custom tokenizer function.
Time complexity is: O(n) where n is the number of chunks of the content of the file.
args
    text_file_path (string) - path to the file

return
    stream of list of tokenized string

"""
def tokenize(text_file_path):
    cnt = 1
    complied_regex = reg_ex_compile()
    for small_chunk_text in read_file_in_chunks(text_file_path):
        tokenized_str = text_to_token(complied_regex, small_chunk_text) 
        yield tokenized_str


"""
Computes the token frequency from a token list.
Time complexity is: O(n) where n is the size of token list.

args
    A single token list.

return
    dictionary { key: Token, value: Count }
"""
def compute_word_frequency(tokens):
    tmp_count = dict()
    cur_token = ''
    jump = 0
    need_jump = False
    i = 0
    for i in range(len(tokens)):
        if need_jump:
            jump -= 1
            if jump == 0:
                need_jump = False
            continue
        
        cur_token = tokens[i]
        if cur_token in [None, ' ', ''] or cur_token.__contains__('\n'): 
            continue

        cur_token = cur_token.lower()
        try:
            if tokens[i + 1] in ['@', '#', '*', '&', "'"]:
                cur_token = cur_token + tokens[i + 1] + tokens[i + 2]
                need_jump = True
                jump = 2
        except:
            continue

        if len(cur_token) < 2 and cur_token not in ['@', '#', '*', '&', "'"]:
            continue

        if cur_token not in tmp_count:
            tmp_count[cur_token] = 0
        
        tmp_count[cur_token] += 1

        cur_token = ''

    return tmp_count



"""
combines the list of dictionarys to a single compiled dictionary and 
sorts it with respect to count value. Then prints it in the following format:
<token>\t<Count>

The following function has the following complexity:  O(n^2) + O(nlog n)

O(n^2): Worst case scenario for the nested for-loops to merge all the dictionaries into one dictionary.
O(nlog n): worst case scenario for the sorted() function which uses the Tim Sort

args

return

"""
def print_token_count():  # TODO ::  change this to print
    if complete_token_count_list.__len__() == 0:
        return

    res = complete_token_count_list[0]
    for token_count_dict in complete_token_count_list[1:]:
        for k in token_count_dict.keys():
            if k not in res:
                res[k] = 0
            res[k] += token_count_dict[k]
    
    res = sorted(res.items(), key=lambda x: x[1], reverse=True)

    for k, cnt in res:
        print(f"{k}\t{cnt}")


# ------------------ HELPER FUNCTIONS ------------------ #
"""
Read the file in chunks. This had to be done so that huge files could be read.
The optimum chunk size was found to be 3500000.
Time complexity is: O(n) where n is the number of chunks of the content of the file.

args
    text_file_path (string) - path to the file

return
    stream of chunks as read from file

"""
def read_file_in_chunks(text_file_path):
    cnt = 2
    with open(text_file_path, mode="r", encoding="utf-8-sig") as f:
        last_space = 0
        left_out_str = ''
        #  TODO :: Change CHUNK SIZE TO OPTIMUM SIZE
        while chunk := f.read(Constants.CHUNK_SIZE):
            last_space = chunk.rfind(' ')
            curr_chunk = left_out_str + chunk[:last_space]
            left_out_str = chunk[last_space:]
            yield curr_chunk


"""
Compile regular expression to help with the split.
Time complexity is: O(1) to generate the regex tree
args

return
    Pattern object - complied regular expression

"""
def reg_ex_compile():
    reg_ex = []
    reg_ex.append(r'([a-zA-Z0-9]+)')
    reg_ex.append(r'\n')
    reg_ex = "|".join(reg_ex)
    return re.compile(reg_ex)


"""
Convert text to token using compiled regex
Time complexity is: O(n) where n is the string in each chunks.
args
    Pattern object, string to split

return
    list of tokenized string

"""
def text_to_token(complied_regex, text):
    res = complied_regex.split(text)
    return res


# ------------------ MAIN FUNCTIONS ------------------ #
if __name__ == '__main__':
    file_name = sys.argv[1]
    if os.path.exists(file_name):
        for tokenized_str in tokenize(file_name):
            r = compute_word_frequency(tokenized_str)
            complete_token_count_list.append(r)
        print_token_count()
