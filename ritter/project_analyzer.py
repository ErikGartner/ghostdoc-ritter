import json

from .analyzerbase import AnalyzerBase
from .analytics.network_analyzer import NetworkAnalyzer


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
            return

        data = {}
        res = self._analyze_networks(project)
        if res is False:
            return False
        self._save_analytics(self.collection, data, project['_id'])
        return True

    def _analyze_networks(self, project):
        print(' => Analyzing network structure')
        ritterData = self.db['ritterData'].find(
            {'project': project['_id'],
             'type': 'source_analytics'})
        texts = self.db['texts'].find({'project': project['_id']})
        if ritterData.count() != texts.count():
            return False

        marked_tree = []
        for data in ritterData:
            if 'marked_tree' not in data['data'] or not data['data'][
                    'marked_tree']['is_linkified']:
                print('\t\t - Error missing marked_tree data')
                return False
            marked_tree.extend(data['data']['marked_tree']['data'])

        pairs = NetworkAnalyzer.count_artifacts_pairs(marked_tree)
        centrality = NetworkAnalyzer.calculate_artifacts_centrality(pairs)
        communities = NetworkAnalyzer.determine_communities(pairs)

        # Mongo can't handle tuple for keys
        jspairs = {}
        for pair in pairs:
            p1 = pair[0]
            p2 = pair[1]
            count = jspairs.get(p1, {})
            count[p2] = pairs[pair]
            jspairs[p1] = count

        data = {
            'pair_occurences': jspairs,
            'centrality': centrality,
            'communities': communities,
        }
        return {'network_analytics': data}
