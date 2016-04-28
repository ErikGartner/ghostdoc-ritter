import re
from collections import Counter
import itertools

from sentimental import sentimental


class SentimentAnalyzer():

    _sentimental = sentimental.Sentimental(max_ngrams=3)
    path = sentimental.Sentimental.get_datafolder()
    _sentimental.train([path + '/sv/lexicon'])

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
                    scores[pair] = scores.get(pair, 0) + senti

        return dict(scores)

    def sentiment(text):
        pos = SentimentAnalyzer._sentimental.sentiment(text)['positive']
        if pos < 0.48:
            return -1
        elif pos > 0.52:
            return 1
        else:
            return 0
