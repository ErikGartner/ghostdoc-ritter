import re
from collections import Counter


class InteractionsAnalyzer:

    def _count_artifacts(marked_tree):
        reg = re.compile('\(([\w]+) \\\"GHOSTDOC-TOKEN\\\"\)')
        counter = Counter()
        for item in marked_tree:
            if 'text' in item:
                m = reg.findall(item['text'])
                c = Counter(m)
                counter = counter + c
        return dict(counter)
