import re
import pprint
import copy


class ArtifactExtractor:

    def extract(marked_tree, artifact):
        filterer = ParseTreeFilterer(artifact['tokens'])
        return filterer.filter(marked_tree)


class ParseTreeFilterer:

    def __init__(self, tokens):
        reg = r'(\b' + r'|\b'.join(tokens) + r')'
        self.artifact_reg = re.compile(reg, re.IGNORECASE)

    def filter(self, mt):
        mt = copy.copy(mt)
        self._filter(mt, 0, len(mt) - 1)
        return [item for item in mt if item is not None]

    def _filter(self, mt, pos, end_pos):
        """
        Returns False is all is None in [pos, end_pos] else True
        """
        start_pos = pos
        while pos <= end_pos:
            item = mt[pos]

            if item is None:
                pos += 1
                continue

            if item['type'] == 'heading':
                pos = self._filter_heading(mt, pos)

            elif item['type'] == 'space':
                mt[i] = None
                pos += 1

            elif item['type'] == 'paragraph':
                pos = self._filter_text(mt, pos)

            elif item['type'] == 'text':
                pos = self._filter_text(mt, pos)

            elif item['type'] == 'list_start':
                pos = self._filter_list(mt, pos)

            else:
                print("Unexpected type: %s" % mt[pos])
                pos += 1

        for p in range(start_pos, end_pos + 1):
            if mt[p] is not None:
                return True
        else:
            return False

    def _artifact_found(self, text):
        return self.artifact_reg.search(text) is not None

    def _filter_heading(self, mt, pos):
        if self._artifact_found(mt[pos]['text']):
            # Artifact was found in heading, keep heading regardless of if
            # there exists any references in text under
            return pos + 1

        # Find end of this section
        end_pos = pos
        while(end_pos + 1 < len(mt) and
              mt[end_pos + 1]['type'] != 'heading'):
            end_pos += 1

        if end_pos == pos:
            # Remove a dangling header
            mt[pos] = None
            return end_pos

        empty_section = not self._filter(mt, pos + 1, end_pos)
        if empty_section:
            mt[pos] = None
        return end_pos + 1

    def _filter_text(self, mt, pos):
        if not self._artifact_found(mt[pos]['text']):
            mt[pos] = None
        return pos + 1

    def _filter_list(self, mt, pos):
        start_pos = pos
        list_empty = True
        while pos < len(mt):
            if mt[pos]['type'] == 'text':
                if not self._artifact_found(mt[pos]['text']):
                    pos += 1
                else:
                    list_empty = False

            elif mt[pos]['type'] == 'list_end':
                if list_empty:
                    for p in range(start_pos, pos + 1):
                        mt[p] = None
                return pos + 1

            pos += 1

        return pos
