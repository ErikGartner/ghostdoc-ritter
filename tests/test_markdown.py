import unittest

from ritter.markdown import MarkdownMixin


class MarkdownMixinTest(unittest.TestCase):

    def test_to_text(self):
        doc = '# Title'
        mdm = MarkdownMixin()
        text = mdm.markdown_to_text(doc)
        self.assertEquals('Title', text)
