from bs4 import BeautifulSoup


# Extract Datas
def separate_data(web_content, url, encoding, nlp_module):
    soup = BeautifulSoup(web_content, 'html.parser')
    # Meta data
    meta_data = soup.findAll("meta")
    # Text data
    text_data = soup.text
    links_data = soup.find_all('a', href=True)
    # Links in the page
    links = []
    for link in links_data:
        l = link["href"]
        ind = l.find('#')
        if ind != -1:
            links.append(l[:ind])
        else:
            links.append(l)
