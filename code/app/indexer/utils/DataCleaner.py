from bs4 import BeautifulSoup


# Extract Datas
def separate_data(web_content, url, encoding, nlp):
    soup = BeautifulSoup(web_content, 'html.parser')
    data = dict()
    # Meta data
    meta_content_type, meta_content_charset, meta_keywords, meta_authors, meta_others = get_all_meta_data(soup, nlp)
    text_data = get_text_from_page(soup, nlp)
    links = get_links_from_page(soup)

    return meta_content_type, meta_content_charset, meta_keywords, meta_authors, meta_others, text_data, links


def get_text_from_page(soup, nlp):
    return nlp.word_tokenizer_count(soup.text)


def get_links_from_page(soup):
    links = []
    links_data = soup.find_all('a', href=True)
    # Links in the page

    for link in links_data:
        l = link["href"]
        ind = l.find('#')
        if ind != -1:
            links.append(l[:ind])
        else:
            links.append(l)

    return links


def get_all_meta_data(soup, nlp):
    meta_data = soup.findAll("meta")
    content_type = []
    content_charset = []
    keywords = []
    authors = []
    others = []
    for tag in meta_data:
        attributes = tag.attrs
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
        else:
            others = others + list(nlp.word_tokenizer_count(attributes['content']).keys())

    return content_type, content_charset, keywords, authors, others
