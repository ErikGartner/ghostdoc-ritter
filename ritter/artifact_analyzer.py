from .analyzerbase import AnalyzerBase
from .analytics.genderize import Genderize


class ArtifactAnalyzer(AnalyzerBase):

    def __init__(self, db, data):
        self.db = db
        self.ritter_type = 'artifact_analytics'
        self.id = data['id']
        self.collection = 'artifacts'

    def analyze(self):
        artifact = self._get_doc(self.collection, self.id)
        if artifact is None:
            print('Artifact not found %s' % self.id)
            return

        data = {}
        data.update(self._determine_gender(artifact))

        self._save_analytics(self.collection, data, artifact.project)
        print('ArtifactAnalyzer done with %s' % artifact['name'])

    def _determine_gender(self, artifact):
        full_name = artifact['name']
        firstname = full_name.split()[0]
        (gender, probability) = Genderize.guess_from_name(firstname)
        return {'genderize': {'gender': gender}}
