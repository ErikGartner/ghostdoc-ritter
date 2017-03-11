import json

from .analyzerbase import AnalyzerBase
from .analytics.genderize import Genderize
from .dataprocessors.artifact_extractor import ArtifactExtractor
from .dataprocessors.toc_generator import TocGenerator
from .dataprocessors.markdown import Markdown
from .dataprocessors.gem_extractor import GemExtractor
from .dataprocessors.annotators import ArtifactAnnotator


class ArtifactAnalyzer(AnalyzerBase):
    def __init__(self, db, data):
        self.db = db
        self.ritter_type = 'artifact_analytics'
        self.id = data['id']
        self.collection = 'artifacts'

    def analyze(self):
        artifact = self._get_doc(self.collection, self.id)
        if artifact is None:
            print('=> Artifact not found %s' % self.id)
            return True

        data = {}
        data.update(self._extract_text(artifact))
        data.update(self._determine_gender(artifact))
        data.update(self._generate_toc(data))
        data.update(self._extract_gems(artifact, data))
        data.update(self._linkify_artifacts(artifact, data))

        self._save_analytics(self.collection, data, artifact['project'])
        return True

    def _determine_gender(self, artifact):
        print(' => Determining gender')
        full_name = artifact['name']
        firstname = full_name.split()[0]
        gender = Genderize.guess_from_name(firstname)
        return {'genderize': {'gender': gender}}

    def _extract_text(self, artifact):
        print(' => Extracting data from sources')
        sources = self.db['texts'].find({'project': artifact['project']})
        data = []
        for source in sources:
            marked_tree = json.loads(source['markedTree'])
            tree = ArtifactExtractor.extract(marked_tree, artifact)
            if len(tree) > 0:
                data.append({'source': source['_id'], 'tree': tree})
        return {'marked_tree': {'data': data}}

    def _generate_toc(self, data):
        print(' => Generating table of content')
        if 'marked_tree' not in data:
            print('\t\t - Error missing marked_tree data')
            return {}

        toc = []
        for d in data['marked_tree']['data']:
            marked_tree = d['tree']
            toc.extend(TocGenerator.generate_toc(marked_tree))

        data = {'toc': {'data': toc}}
        return data

    def _extract_gems(self, artifact, data):
        print(' => Extracting gems')
        if 'marked_tree' not in data:
            print('\t\t - Error missing marked_tree data')
            return {}

        artifacts = iter(self.db['artifacts'].find(
                            {'project': artifact['project']}))

        tree = []
        for d in data['marked_tree']['data']:
            tree.extend(d['tree'])

        gems = iter(self.db['gems'].find({'project': artifact['project']}))
        gem_data = GemExtractor.extract(tree, artifact, gems, artifacts)

        data = {'gems': {'data': gem_data}}
        return data

    def _linkify_artifacts(self, artifact, data):
        print(' => Linkifying artifacts')
        if 'marked_tree' not in data:
            print('\t\t - Error missing marked_tree data')
            return {}

        artifacts = self.db['artifacts'].find({'project': artifact['project']})
        artifacts = iter(artifacts)

        marked_tree = []
        for item in data['marked_tree']['data']:
            marked_tree.extend(item['tree'])

        ArtifactAnnotator.linkify_artifacts(marked_tree, artifacts)
        data['marked_tree']['is_linkified'] = True
        return {}
