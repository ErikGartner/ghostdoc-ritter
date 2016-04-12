import re


class GemExtractor:
    def sentence_reg(tokens):
        reg = '([^.?!]*(?:' + '|'.join(tokens) + ')[^.?!]*)'
        return re.compile(reg, re.IGNORECASE)

    def capture_reg(pattern):
        return re.compile(pattern, re.IGNORECASE)

    def extract_gem(text, gem, artifact):
        results = []
        if gem is None:
            return None

        reg_sentences = GemExtractor.sentence_reg(artifact['tokens'])

        sentences = reg_sentences.findall(text)
        if len(sentences) == 0:
            return None

        for pattern in gem['patterns']:
            reg_capture = GemExtractor.capture_reg(pattern)
            for sentence in sentences:
                match = reg_capture.findall(sentence)
                if len(match) != 0:
                    results.extend(match)

        if len(results) > 0:
            return {'name': gem['name'], 'result': results}
        else:
            return None
