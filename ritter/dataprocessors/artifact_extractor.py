import re


class ArtifactExtractor:

    def extract(marked_tree, artifact):
        data = []

        header = None
        for item in marked_tree:
            # preserve last header and append it later
            if item['type'] == 'heading':
                header = item

            elif item['type'] == 'paragraph':
                reg = ArtifactExtractor._paragraph_reg(artifact['tokens'])
                if reg.search(item['text']) is not None:
                    if header is not None:
                        data.append(header)
                        header = None
                    data.append(item)

        return data

    def _paragraph_reg(tokens):
        reg = r'(\b' + r'|\b'.join(tokens) + r')'
        return re.compile(reg, re.IGNORECASE)
