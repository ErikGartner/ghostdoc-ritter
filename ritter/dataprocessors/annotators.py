import re


class ArtifactAnnotator:

    def linkify_artifacts(marked_tree, artifacts):
        for artifact in artifacts:
            link = '(%s "GHOSTDOC-TOKEN")' % artifact['_id']
            for token in artifact['tokens']:
                reg = ArtifactAnnotator._token_reg(token)
                for item in marked_tree:
                    if 'text' in item:
                        repl = r'[\1]%s' % link
                        item['text'] = reg.sub(repl, item['text'])

        return marked_tree

    def _token_reg(token):
        reg = r'(\b%s)' % token
        return re.compile(reg, re.IGNORECASE)
