import re


'''
token can be defined as collections of  [a-zA-Z0-9@#*&'], 
any other signs and charterers should be considered as an separator.
'''


class MyTokenizer:
    def __init__(self):
        # self.regex = r"[.|!|>]|^[@|#|*|&|']| " # partially working
        self.token_spec = [
            r"(?=!)",
            r"\s",
            r"([@|#|*|&|']\s*)"
            # r"^[@|#|*|&|']",  # non-separator
            # r"(?=\w+[^@]\w+)",  # non-separator
            # r' ',  # spaces
            # r'\n'  # New line
        ]
        self.regex = '|'.join(self.token_spec)

    def my_tokenizer(self, s: str, token_word_count: dict):
        res_token = dict(token_word_count)
        res = re.split(self.regex, s.lower(), flags=re.I | re.M | re.MULTILINE)
        for r in res:
            if r not in res_token:
                res_token[r] = 0
            res_token[r] += 1

        for k in res_token.keys():
            if k not in token_word_count:
                token_word_count[k] = 0
            token_word_count[k] += res_token[k]

        print(res_token.keys())


# TODO :: DELETE :: Tokenizer local tester
if __name__ == '__main__':
    m = MyTokenizer()
    m.my_tokenizer("info@com! it's a great day.", dict())  # ['info@com', '!', "it's", 'a', 'great', 'day']
    m.my_tokenizer("abce>def", dict())  # [‘abcd’, ‘>’, ‘def’]
    m.my_tokenizer("abce#def", dict())  # [‘abcd#def’]
    m.my_tokenizer("abce&def", dict())  # [‘abcd&def’]
    m.my_tokenizer("""This eBook is for the use of anyone anywhere in the United States and
most other parts of the world at no cost and with almost no restrictions
whatsoever. You may copy it, give it away or re-use it under the terms
of the Project Gutenberg License included with this eBook or online at
www.gutenberg.org. THis is the.""", dict())

"""
'abce>def'  -> [‘abcd’, ‘>’, ‘def’]
'info@com! it's a great day' -> ['info@com', '!', "it's", 'a', 'great', 'day']
"""
