from sentimental.sentimental import Sentimental


class SentimentAnalyzer():

    _sentimental = Sentimental(max_ngrams=3)
    _sentimental.train(['data/sv/lexicon'])

    def count_artifacts_pairs(marked_tree):
        reg = re.compile('\(([\w]+) \\\"GHOSTDOC-TOKEN\\\"\)')
        counter = Counter()
        for item in marked_tree:
            if 'text' in item:
                sentiment = SentimentAnalyzer.sentiment(item['text'])
                m = reg.findall(item['text'])
                c = list(Counter(m))
                c.sort()
                pairs = list(itertools.combinations(c, 2))
                counts = Counter(pairs)
                counter = counter + counts
        return dict(counter)

    def sentiment(text):
        return _sentimental.sentiment(text)
