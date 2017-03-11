import re


class GemExtractor:

    GHMACRO_THIS_ARTIFACT = "~GH_THIS_ARTIFACT~"
    GHMACRO_OTHER_ARTIFACT = "~GH_OTHER_ARTIFACT~"

    _sentence_reg = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')

    def extract(tree, artifact, gems, artifacts):
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
            g = GemExtractor.extract_gem(sentences, gem, artifact, artifacts)
            if g is not None:
                data.append(g)

        return data

    def extract_gem(sentences, gem, artifact, artifacts):
        results = []
        if gem is None:
            return None

        for pt in gem['patterns']:
            pattern = GemExtractor._apply_macros(pt, gem, artifact, artifacts)
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

    def _no_capture_token_reg(tokens):
        return r'(?:\b' + r'|\b'.join(tokens) + r')'

    def _apply_macros(pattern, gem, artifact, artifacts):
        pt = pattern

        # GHMACRO_THIS_ARTIFACT
        pt = pt.replace(GemExtractor.GHMACRO_THIS_ARTIFACT,
                        GemExtractor._no_capture_token_reg(artifact['tokens']))

        # GHMACRO_OTHER_ARTIFACT
        if GemExtractor.GHMACRO_OTHER_ARTIFACT in pattern:
            artifacts = list(artifacts)
            other_tokens = [a['tokens'] for a in artifacts]
            other_tokens = [item for subl in other_tokens for item in subl]
            pt = pt.replace(GemExtractor.GHMACRO_OTHER_ARTIFACT,
                            GemExtractor._no_capture_token_reg(other_tokens))

        return pt
