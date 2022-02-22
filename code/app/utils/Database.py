import json


def get_data(trie_controller, prefix):
    # res = trie_controller.search_prefix(str(prefix))
    # res = sorted(res, key=lambda x: x[1], reverse=True)
    res = [
        {'title': 'Title 1', 'tags': '#tags1', 'last_updated': '1', 'url': '#'}
    ]
    # result = []
    # for r in res[:50]:
    #     web_dict_data = json.load(r[0])
    #     url = web_dict_data['url']
    #     web_content = web_dict_data['content']
    #     encoding = web_dict_data['encoding']
    #     result.append({
    #         'title': url , 'tags': r[0], 'last_updated': '10', 'url': url
    #     })
    return res
