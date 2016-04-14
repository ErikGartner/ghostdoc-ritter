import json

from .analyzerbase import AnalyzerBase
from .dataprocessors.toc_generator import TocGenerator


class SourceAnalyzer(AnalyzerBase):

    def __init__(self, db, data):
        self.db = db
        self.ritter_type = 'source_analytics'
        self.id = data['id']
        self.collection = 'texts'

    def analyze(self):
        text = self._get_doc(self.collection, self.id)
        if text is None:
            print(' => Text not found %s' % self.id)
            return

        marked_tree = json.loads(text['markedTree'])

        data = {}
        data.update(self._generate_toc(marked_tree))
        self._save_analytics(self.collection, data, text['project'])

    def _generate_toc(self, marked_tree):
        print(' => Generating table of content')
        data = {
            'toc': TocGenerator.generate_toc(marked_tree)
        }
        return data
