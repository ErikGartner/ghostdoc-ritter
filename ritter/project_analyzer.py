import json

from .analyzerbase import AnalyzerBase
from .analytics.network_analyzer import NetworkAnalyzer
from .dataprocessors.annotators import ArtifactAnnotator


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
        data.update(self._analyze_networks(project))
        self._save_analytics(self.collection, data, project['_id'])
        return True

    def _analyze_networks(self, project):
        # This needs to be speeded up since it re-annotates all artifacts again
        print(' => Analyzing network structure')
        sources = self.db['texts'].find({'project': project['_id']})

        marked_tree = []
        for source in sources:
            if 'markedTree' not in source:
                print('\t\t - Error missing marked_tree data')
                return {}
            marked_tree.extend(json.loads(source['markedTree']))

        artifacts = self.db['artifacts'].find({'project': project['_id']})
        artifacts = iter(artifacts)

        ArtifactAnnotator.linkify_artifacts(marked_tree, artifacts)

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
            count = jspairs.get(p2, {})
            count[p1] = pairs[pair]
            jspairs[p2] = count

        data = {
            'pair_occurences': jspairs,
            'centrality': centrality,
            'communities': communities,
        }
        return {'network_analytics': data}
