import json

from .analyzerbase import AnalyzerBase
from .analytics.genderize import Genderize
from .dataprocessors.artifact_extractor import ArtifactExtractor


class ArtifactAnalyzer(AnalyzerBase):
    def __init__(self, db, data):
        self.db = db
        self.ritter_type = 'artifact_analytics'
        self.id = data['id']
        self.collection = 'artifacts'

    def analyze(self):
        print('\t Running ArtifactAnalyzer')
        artifact = self._get_doc(self.collection, self.id)
        if artifact is None:
            print('=> Artifact not found %s' % self.id)
            return

        data = {}
        data.update(self._extract_text(artifact))
        data.update(self._determine_gender(artifact))

        self._save_analytics(self.collection, data, artifact['project'])
        print('\t ArtifactAnalyzer done with %s' % artifact['name'])

    def _determine_gender(self, artifact):
        print('\t => Determining gender')
        full_name = artifact['name']
        firstname = full_name.split()[0]
        gender = Genderize.guess_from_name(firstname)
        return {'genderize': {'gender': gender}}

    def _extract_text(self, artifact):
        print('\t => Extracting data from sources')
        sources = self.db['texts'].find({'project': artifact['project']})
        data = []
        for source in sources:
            marked_tree = json.loads(source['markedTree'])
            tree = ArtifactExtractor.extract(marked_tree, artifact)
            if len(tree) > 0:
                data.append({'source': source['_id'], 'tree': tree})
        return {'marked_tree': {'data': data}}
