import re


class ArtifactAnnotator:

    excluded_types = set(['heading', 'code'])

    def linkify_artifacts(marked_tree, artifacts):
        big_string = ArtifactAnnotator._marked_tree_to_big_string(marked_tree)

        for artifact in artifacts:
            link = '(%s "GHOSTDOC-TOKEN")' % artifact['_id']
            for token in artifact['tokens']:
                reg = ArtifactAnnotator._token_reg(token)
                repl = r'[\1]%s' % link
                big_string = reg.sub(repl, big_string)

        ArtifactAnnotator._big_string_to_marked_tree(marked_tree, big_string)
        return marked_tree

    def _token_reg(token):
        reg = r'(\b%s)' % token
        return re.compile(reg, re.IGNORECASE)

    def _marked_tree_to_big_string(marked_tree):
        strings = []
        for item in marked_tree:
            if 'text' in item and item['type'] not in ArtifactAnnotator.excluded_types:
                strings.append(item['text'])
        big_string = u'\u1394'.join(strings)
        return big_string

    def _big_string_to_marked_tree(marked_tree, big_string):
        strings = big_string.split(u'\u1394')
        i = 0
        for item in marked_tree:
            if 'text' in item and item['type'] not in ArtifactAnnotator.excluded_types
                item['text'] = strings[i]
                i = i + 1
