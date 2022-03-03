def clean_data(prefix, data):
    res = []
    ln = len(prefix)
    for d in data:
        try:
            tmp = d.split('\t')
            if len(tmp) < 4:
                continue
            # get similarity score
            dist = anti_distance(tmp[0], prefix, ln)
            tmp[2] = int(tmp[2])
            res.append(
                {
                    'title': tmp[1],
                    'tags': [tmp[0]],
                    'url': tmp[1],
                    'score': tmp[2],
                    'distance': dist
                }
            )
        except Exception as e:
            print('ERROR: ', d)
            print(e.args)

    # res = sorted(res, key=lambda x: (x['tags'], 1.0/x['score']), reverse=False)
    res = sorted(res, key=lambda x: (x['distance'], x['score']), reverse=True)
    return res[:25]


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
