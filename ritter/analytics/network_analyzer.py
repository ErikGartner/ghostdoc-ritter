import re
from collections import Counter
import itertools

import networkx as nx
import community


class NetworkAnalyzer:

    def calculate_artifacts_centrality(pair_counts):
        """This uses PageRank to determine artifacts centrality."""
        g = nx.Graph()
        for pair in pair_counts:
            g.add_edge(pair[0], pair[1], weight=pair_counts[pair])
        pr = nx.pagerank_numpy(g)
        return pr

    def determine_communities(pair_counts):
        g = nx.Graph()
        for pair in pair_counts:
            g.add_edge(pair[0], pair[1], weight=pair_counts[pair])
        com = community.best_partition(g)
        print(com)
        return com

    def count_artifacts_pairs(marked_tree):
        reg = re.compile('\(([\w]+) \\\"GHOSTDOC-TOKEN\\\"\)')
        counter = Counter()
        for item in marked_tree:
            if 'text' in item:
                m = reg.findall(item['text'])
                c = Counter(m)
                pairs = list(itertools.combinations(list(c), 2))
                counts = Counter(pairs)
                counter = counter + counts
        return dict(counter)
