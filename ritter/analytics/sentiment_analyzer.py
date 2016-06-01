import re, math
from collections import Counter
import itertools

from sentimental import Sentimetanl, get_datafolder


class SentimentAnalyzer():

    _sentimental = Sentimental(max_ngrams=2, undersample=True)
    _sentimental.train([get_datafolder() + '/sv/ruhburg'])

    def calculate_friend_scores(marked_tree):
        reg = re.compile('\(([\w]+) \\\"GHOSTDOC-TOKEN\\\"\)')
        scores = {}
        for item in marked_tree:
            if 'text' in item:
                m = reg.findall(item['text'])
                c = sorted(list(Counter(m)))
                pairs = list(itertools.combinations(c, 2))

                senti = SentimentAnalyzer.sentiment(item['text'])
                for pair in pairs:
                    s = scores.get(pair, [0, 0])
                    if senti == 1:
                        s[0] = s[0] + 1
                    elif senti == -1:
                        s[1] = s[1] + 1
                    scores[pair] = s

        return {_id: (vals[0] - vals[1]) * math.exp(max(vals) / (vals[0] + vals[1] + 1)) for _id, vals in scores.items()}

    def sentiment(text):
        label = max(SentimentAnalyzer._sentimental.sentiment(text))
        if label == 'positive':
            return 1
        elif label == 'negative':
            return -1
        else:
            return 0
