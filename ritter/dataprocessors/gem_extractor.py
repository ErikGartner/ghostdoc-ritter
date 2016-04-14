import re


class GemExtractor:

    def extract(text, artifact, gems):
        data = []

        reg_sentences = GemExtractor._sentence_reg(artifact['tokens'])
        sentences = reg_sentences.findall(text)
        if len(sentences) == 0:
            return data

        for gem in gems:
            gem_data = GemExtractor.extract_gem(sentences, gem, artifact)
            data.append(gem_data)

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

    def _sentence_reg(tokens):
        reg = '([^.?!]*(?:' + '|'.join(tokens) + ')[^.?!]*)'
        return re.compile(reg, re.IGNORECASE)

    def _capture_reg(pattern):
        return re.compile(pattern, re.IGNORECASE)
