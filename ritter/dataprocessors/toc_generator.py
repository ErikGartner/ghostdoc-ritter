import re


class TocGenerator:

    def generate_toc(marked_tree):
        regex = re.compile(r'[^A-Za-z0-9_]+')
        toc = []
        for item in marked_tree:
            if item['type'] == 'heading':
                t = 'header-' + regex.sub('-', item['text']).lower()
                c = item.copy()
                c.update({'id': t})
                toc.append(c)
        return toc
