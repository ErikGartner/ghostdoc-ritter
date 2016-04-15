import re


class GemExtractor:

    _sentence_reg = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')

    def extract(tree, artifact, gems):
        token_reg = GemExtractor._token_reg(artifact['tokens'])
        sentences = []
        for item in tree:
            if 'text' in item:
                sub_sents = GemExtractor._sentence_reg.split(item['text'])
                for s in sub_sents:
                    if token_reg.search(s) is not None:
                        sentences.append(s)

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

    def _token_reg(tokens):
        reg = r'(\b' + r'|\b'.join(tokens) + r')'
        return re.compile(reg, re.IGNORECASE)
