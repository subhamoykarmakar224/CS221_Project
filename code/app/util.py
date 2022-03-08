import math
from fuzzywuzzy import fuzz


# Class to aggregate all the fields we need to track
class SearchResult:
    def __init__(self, url, term, tfidf, query_token) -> None:
        self.url = url
        self.terms = [term]
        self.tfidf = tfidf
        self.query_tokens = [query_token]

        # scales down the weight of the string similarity between
        # terms and query tokens to give more weight to tfidf
        self.alpha = 2

    def similarity_ratio(self):
        ratios = []

        for (term, query_token) in zip(self.terms, self.query_tokens):
            ratios.append(fuzz.partial_ratio(term, query_token))

        return ratios

    def scaled_similarity(self):
        return sum(self.similarity_ratio()) / self.alpha


def clean_data(query_tokens, search_results):
    results_by_token = dict()

    # using this hardcoded value for number of documents indexed
    N = 55393
    

    # 1: Calculate all the tf-idfs for each found document for each query token
    # Note: 'term' refers to a similar prefix found in the inverted index, for example:
    # query token: 'cristina' --> term: 'critic'
    for token in query_tokens:
        results_by_token[token] = dict()
        m = len(search_results[token])

        for d in search_results[token]:
            try:
                tmp = d.split('\t')

                url = tmp[1]

                if len(tmp) < 4 or url in results_by_token[token]:
                    continue

                tf = 1 + math.log(int(tmp[2]))
                idf = math.log(N / m)

                results_by_token[token][url] = SearchResult(url, tmp[0], tf*idf, token)
        
            except Exception as e:
                print('ERROR: ', d)
                print(e.args)


    # 2: only take documents that contained terms for ALL query tokens
    intersection = results_by_token[query_tokens[0]].keys()
    for i in range(len(query_tokens)):
        intersection = intersection & results_by_token[query_tokens[i]].keys()


    # 3. Aggregate the SearchResult objects by adding the terms, query_tokens, and tf-idfs for 
    # each occurance of the document
    results_by_url = dict()
   
    for token in query_tokens:

        for url in intersection:

            if url in results_by_token[token]:

                if url not in results_by_url:
                    results_by_url[url] = results_by_token[token][url]
                else:
                    results_by_url[url].terms += results_by_token[token][url].terms
                    results_by_url[url].query_tokens += results_by_token[token][url].query_tokens
                    results_by_url[url].tfidf += results_by_token[token][url].tfidf


    # 4. Return results sorted by tf-idf + similarity of terms to query tokens
    to_return = []
    for url in sorted(results_by_url, key = lambda u: -(results_by_url[u].tfidf + results_by_url[u].scaled_similarity())):
        to_return.append(  
            {
                'title': results_by_url[url].url,
                'tags': results_by_url[url].terms,
                'score': results_by_url[url].tfidf,
                'distance': results_by_url[url].similarity_ratio()
            }
        )

    # res = sorted(res, key=lambda x: (x['tags'], 1.0/x['score']), reverse=False)
    return to_return[:25]


def anti_distance(s1, s2, ln):
    return sum(1 for (a, b) in zip(s1, s2) if a == b)

# anti_distance('subhamoy', 'subas', len('subha'))

# ['levorato||https://www.cs.uci.edu/dutt-levorato-awarded-nsf-grant-for-healthcare-iot-research/||6||[28, 2667, 2837, 2893, 3102, 3177]||\n',...
# res = [
#     {'title': 'T1', 'tags': '#tag1', 'last_updated': '-na-', 'url': 'http://test1.html'},
#     {'title': 'T2', 'tags': '#tag2',
#         'last_updated': '-na-', 'url': 'http://test2.html'},
#     {'title': 'T3', 'tags': '#tag3',
#         'last_updated': '-na-', 'url': 'http://test3.html'},
#     {'title': 'T4', 'tags': '#tag4',
#         'last_updated': '-na-', 'url': 'http://test4.html'}
# ]
# l = ['levorato||https://www.cs.uci.edu/dutt-levorato-awarded-nsf-grant-for-healthcare-iot-research/||6||[28, 2667, 2837, 2893, 3102, 3177]||\n', 'levorato||https://www.cs.uci.edu/levorato-collaborates-on-3-7-million-grant-for-electricity-distribution-cybersecurity/||5||[26, 2666, 2772, 2970, 3189]||\n', 'levorato||https://www.cs.uci.edu/pc-mag-inside-darpas-hackfest-at-nasa-research-park-marco-levarato-quoted/||3||[51, 2708, 2914]||\n', 'levorato||https://www.cs.uci.edu/news/page/12/||2||[5449, 5558]||\n', 'levorato||https://www.cs.uci.edu/news/page/14/||1||[3371]||\n', 'levorato||https://www.cs.uci.edu/cs-research-showcase-continues-to-provide-a-platform-for-students-to-showcase-their-work/||1||[3189]||\n', 'levorato||https://www.cs.uci.edu/husky-or-wolf-using-a-black-box-learning-model-to-avoid-adoption-errors/||1||[3109]||\n', 'levorato||https://www.cs.uci.edu/events/list/page/3/?tribe_event_display=past&tribe_paged=4||1||[6004]||\n', 'levorato.||https://www.cs.uci.edu/professor-levoratos-darpa-project-aims-to-strengthen-autonomous-drone-systems/||1||[3358]||\n', 'lewi||https://www.cs.uci.edu/senior-spotlight-uci-sets-up-dante-chakravorti-for-continued-success-in-computer-science-and-volleyball-after-graduation/#more-2080||3||[2910, 3003, 3101]||\n', 'lewi||https://www.informatics.uci.edu/very-top-footer-menu-items/news/page/18/||1||[7134]||\n', 'ley||http://www-db.ics.uci.edu/pages/links/proceedings.shtml||1||[1544]||\n', '', 'leysia||https://www.informatics.uci.edu/gary-olson-2-ics-alums-receive-sigchi-honors/#content||1||[6959]||\n', '', 'leysia||https://www.informatics.uci.edu/gary-olson-2-ics-alums-receive-sigchi-honors/||1||[6959]||\n', '']
# clean_data(l)
