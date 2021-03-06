import json

from .analyzerbase import AnalyzerBase
from .dataprocessors.toc_generator import TocGenerator
from .dataprocessors.annotators import ArtifactAnnotator
from .analytics.lang_detector import LangDetector


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
            return True

        marked_tree = json.loads(text['markedTree'])

        data = {}
        data.update(self._generate_toc(marked_tree))
        data.update(self._linkify_artifacts(marked_tree, text))
        data.update(self._detect_language(text))

        self._save_analytics(self.collection, data, text['project'])
        return True

    def _generate_toc(self, marked_tree):
        print(' => Generating table of content')
        return {'toc': {'data': TocGenerator.generate_toc(marked_tree)}}

    def _linkify_artifacts(self, marked_tree, text):
        print(' => Linkifying artifacts')

        artifacts = self.db['artifacts'].find({'project': text['project']})
        artifacts = iter(artifacts)

        ArtifactAnnotator.linkify_artifacts(marked_tree, artifacts)
        return {'marked_tree': {'data': marked_tree, 'is_linkified': True}}

    def _detect_language(self, text):
        print(' => Detecing language')
        return {'lang_detector': {'lang': LangDetector.detect(text['text'])}}
