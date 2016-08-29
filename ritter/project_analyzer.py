import json

from .analyzerbase import AnalyzerBase
from .analytics.network_analyzer import NetworkAnalyzer
from .analytics.sentiment_analyzer import SentimentAnalyzer
from .dataprocessors.annotators import ArtifactAnnotator
from .analytics.trello_source import TrelloSource


class ProjectAnalyzer(AnalyzerBase):
    def __init__(self, db, data):
        self.db = db
        self.ritter_type = 'project_analytics'
        self.id = data['id']
        self.collection = 'projects'

    def analyze(self):
        project = self._get_doc(self.collection, self.id)
        if project is None:
            print(' => Project not found %s' % self.id)
            return True

        sources = self.db['texts'].find({'project': project['_id']})

        # Linkify marked_tree
        marked_tree = []
        for source in sources:
            if 'markedTree' not in source:
                print('\t\t - Error missing marked_tree data')
                return {}
            marked_tree.extend(json.loads(source['markedTree']))

        artifacts = list(self.db['artifacts'].find({'project': project['_id']}))
        ArtifactAnnotator.linkify_artifacts(marked_tree, artifacts)

        data = {}
        data.update(self._analyze_networks(marked_tree))
        data.update(self._analyze_relations(marked_tree))
        data.update(self._analyze_trello(project, artifacts))
        self._save_analytics(self.collection, data, project['_id'])
        return True

    def _analyze_networks(self, marked_tree):
        print(' => Analyzing network structure')

        pairs = NetworkAnalyzer.count_artifacts_pairs(marked_tree)
        centrality = NetworkAnalyzer.calculate_artifacts_centrality(pairs)
        communities = NetworkAnalyzer.determine_communities(pairs)

        jspairs = ProjectAnalyzer._pairs_to_jspairs(pairs)

        data = {
            'pair_occurences': jspairs,
            'centrality': centrality,
            'communities': communities,
        }
        return {'network_analytics': data}

    def _analyze_relations(self, marked_tree):
        print(' => Analyzing sentiment scores')

        data = SentimentAnalyzer.calculate_scores(marked_tree)
        data['friend_scores'] = ProjectAnalyzer._pairs_to_jspairs(data['friend_scores'])

        return {'relations_analytics': data}

    def _pairs_to_jspairs(pairs):
        # Mongo can't handle tuple for keys
        jspairs = {}
        for pair in pairs:
            p1 = pair[0]
            p2 = pair[1]
            count = jspairs.get(p1, {})
            count[p2] = pairs[pair]
            jspairs[p1] = count
            count = jspairs.get(p2, {})
            count[p1] = pairs[pair]
            jspairs[p2] = count
        return jspairs

    def _analyze_trello(self, project, artifacts):
        print(' => Refreshing Trello source')
        res = TrelloSource.refresh_source(project, artifacts)
        return {
            'trello': res
        }
