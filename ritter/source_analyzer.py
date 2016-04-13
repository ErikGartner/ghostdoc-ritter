from .analyzerbase import AnalyzerBase


class SourceAnalyzer(AnalyzerBase):

    def __init__(self, db, data):
        self.db = db
        self.ritter_type = 'source_analytics'
        self.id = data['id']
        self.collection = 'texts'

    def analyze(self):
        text = self._get_doc(self.collection, self.id)
        if text is None:
            print('Text not found %s' % self.id)
            return

        data = {}

        self._save_analytics(self.collection, data)
        print('SourceAnalyzer done with %s' % text['name'])
