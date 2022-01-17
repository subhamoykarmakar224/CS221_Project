import re


# [a-zA-Z0-9@#*&']
class MyTokenizer:
    def __init__(self):
        # self.regex = r"[.|!|>]|^[@|#|*|&|']| " # partially working
        self.token_spec = [
            r"^[@|#|*|&|']",  # non-separator
            # r"(?=\w+[^@]\w+)",  # non-separator
            r' ',  # spaces
            r'\n'  # New line

        ]
        self.regex = '|'.join(self.token_spec)

    def my_tokenizer(self, s: str):
        res = re.split(self.regex, s, flags=re.I | re.M | re.MULTILINE)
        return res  # TODO: add to dictionary of count of token


# TODO :: DELETE :: Tokenizer local tester
# if __name__ == '__main__':
#     m = MyTokenizer()
#     m.my_tokenizer("info@com! it's a great day.")  # ['info@com', '!', "it's", 'a', 'great', 'day']
#     m.my_tokenizer("abce>def")  # [‘abcd’, ‘>’, ‘def’]
#     m.my_tokenizer("abce#def")  # [‘abcd#def’]
#     m.my_tokenizer("abce&def")  # [‘abcd&def’]
#     m.my_tokenizer("""This eBook is for the use of anyone anywhere in the United States and
# most other parts of the world at no cost and with almost no restrictions
# whatsoever. You may copy it, give it away or re-use it under the terms
# of the Project Gutenberg License included with this eBook or online at
# www.gutenberg.org""")
#
# """
# 'abce>def'  -> [‘abcd’, ‘>’, ‘def’]
# 'info@com! it's a great day' -> ['info@com', '!', "it's", 'a', 'great', 'day']
# """
