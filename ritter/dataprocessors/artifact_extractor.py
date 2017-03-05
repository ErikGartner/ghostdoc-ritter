import re


class ArtifactExtractor:
    def extract(marked_tree, artifact):
        data = []
        reg = ArtifactExtractor._paragraph_reg(artifact['tokens'])
        marked_tree = [i
                       for i in marked_tree
                       if ArtifactExtractor._filter_text_items(i, reg)]

        marked_tree = ArtifactExtractor._filter_headers(marked_tree)
        marked_tree = ArtifactExtractor._rec_filter_lists(marked_tree, 0)
        return marked_tree

    def _paragraph_reg(tokens):
        reg = r'(\b' + r'|\b'.join(tokens) + r')'
        return re.compile(reg, re.IGNORECASE)

    def _filter_text_items(item, reg):
        if 'text' in item and item['type'] != 'heading':
            return reg.search(item['text']) is not None
        elif item['type'] == 'space':
            return False
        else:
            return True

    def _filter_headers(mt):
        for i in range(len(mt) - 1):
            if mt[i] is None:
                continue
            if mt[i]['type'] == mt[i + 1]['type'] == 'heading':
                mt[i] = None
        if len(mt) > 0 and mt[-1].get('type') == 'heading':
            mt[-1] = None
        return [i for i in mt if i != None]

    def _rec_filter_lists(mt, i):
        if i > len(mt) - 1:
            return mt

        if (mt[i]['type'].endswith('_item_start') and
            mt[i + 1]['type'] == 'list_item_end'):
            del mt[i]
            del mt[i + 1]

        elif (mt[i]['type'].endswith('list_start') and
            mt[i + 1]['type'] == 'list_end'):
            del mt[i]
            del mt[i + 1]

        else:
            i += 1

        return ArtifactExtractor._rec_filter_lists(mt, i)
