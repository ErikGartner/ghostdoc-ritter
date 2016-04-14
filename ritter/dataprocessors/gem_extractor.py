import re


class GemExtractor:

    def extract(tree, artifact, gems):
        sentences = []
        for item in tree:
            if 'text' in item:
                sentences.append(item['text'])

        if len(sentences) == 0:
            return []

        data = []
        for gem in gems:
            data.append(GemExtractor.extract_gem(sentences, gem, artifact))

        return data

    def extract_gem(sentences, gem, artifact):
        results = []
        if gem is None:
            return None

        for pattern in gem['patterns']:
            reg_capture = GemExtractor._capture_reg(pattern)
            for sentence in sentences:
                match = reg_capture.findall(sentence)
                if len(match) != 0:
                    results.extend(match)

        if len(results) > 0:
            return {'name': gem['name'], 'result': results}
        else:
            return None

    def _capture_reg(pattern):
        return re.compile(pattern, re.IGNORECASE)
