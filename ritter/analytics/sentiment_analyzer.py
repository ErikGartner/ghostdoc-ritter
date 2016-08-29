import re
import math
from collections import Counter
import itertools

from sentimental import Sentimental, get_data_path


class SentimentAnalyzer():

    _sentimental = Sentimental(max_ngrams=2, undersample=True)
    _sentimental.train([get_data_path() + '/sv/ruhburg'])

    def calculate_scores(marked_tree):
        reg = re.compile('\(([\w]+) \\\"GHOSTDOC-TOKEN\\\"\)')
        friend_scores = {}
        artifact_scores = {}
        for item in marked_tree:
            if 'text' in item:
                senti = SentimentAnalyzer.sentiment(item['text'])
                m = reg.findall(item['text'])
                c = sorted(list(Counter(m)))

                # artifact scores
                for artifacts in c:
                    s = artifact_scores.get(artifacts, [0, 0])
                    if senti == 1:
                        s[0] = s[0] + 1
                    elif senti == -1:
                        s[1] = s[1] + 1
                    artifact_scores[artifacts] = s

                # friend scores
                pairs = list(itertools.combinations(c, 2))
                for pair in pairs:
                    s = friend_scores.get(pair, [0, 0])
                    if senti == 1:
                        s[0] = s[0] + 1
                    elif senti == -1:
                        s[1] = s[1] + 1
                    friend_scores[pair] = s

        friend_scores = {_id: (vals[0] - vals[1]) * math.exp(max(vals) / (vals[0] + vals[1] + 1)) for _id, vals in friend_scores.items()}
        artifact_scores = {_id: (vals[0] - vals[1]) * math.exp(max(vals) / (vals[0] + vals[1] + 1)) for _id, vals in artifact_scores.items()}

        return {
            'friend_scores': friend_scores,
            'artifact_scores': artifact_scores
        }

    def sentiment(text):
        label = max(SentimentAnalyzer._sentimental.sentiment(text))
        if label == 'positive':
            return 1
        elif label == 'negative':
            return -1
        else:
            return 0
