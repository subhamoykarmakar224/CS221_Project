from bs4 import BeautifulSoup

def get_all_meta_data(soup, nlp):
    meta_data = soup.findAll("meta")
    content_type = []
    content_charset = []
    keywords = []
    authors = []
    others = []
    for tag in meta_data:
        attributes = tag.attrs
        try:
            if 'http-equiv' in attributes:
                tmp = str(attributes['content']).split(';')
                content_type = tmp[0].strip(' ')
                content_charset = tmp[1].strip(' ')
            elif 'name' in attributes:
                if attributes['name'] == 'description':
                    keywords = keywords + list(nlp.word_tokenizer_count(attributes['content']).keys())
            elif 'name' in attributes:
                if attributes['name'] == 'author':
                    authors = authors + list(nlp.word_tokenizer_count(attributes['content']).keys())
            # else:
            #     others = others + list(nlp.word_tokenizer_count(attributes).keys())
        except:
            print('Error: ', attributes)

    return content_type, content_charset, keywords, authors, others
