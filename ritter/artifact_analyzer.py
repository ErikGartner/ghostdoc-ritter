from .analyzerbase import AnalyzerBase
from .analytics.genderize import Genderize


class ArtifactAnalyzer(AnalyzerBase):

    def __init__(self, db, data):
        self.db = db
        self.ritter_type = 'artifact_analytics'
        self.id = data['id']

    def analyze(self):
        self._get_artifact()
        if self.artifact is None:
            print('Artifact not found %s' % self.id)
            return

        data = {}
        data.update(self._determine_gender())

        self._save_analytics(data)
        print('ArtifactAnalyzer done with %s' % self.artifact['name'])

    def _determine_gender(self):
        full_name = self.artifact['name']
        firstname = full_name.split()[0]
        (gender, probability) = Genderize.guess_from_name(firstname)
        return {'genderize': {'gender': gender}}

    def _get_artifact(self):
        collection = self.db['artifacts']
        self.artifact = collection.find_one({'_id': self.id})

    def _save_analytics(self, data):
        collection = self.db['ritterData']
        collection.remove({'id': self.ritter_id()})
        doc = {
            'id': self.ritter_id(),
            'type': self.ritter_type,
            'data': data
        }
        collection.insert_one(doc)
