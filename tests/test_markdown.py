import unittest

from ritter.dataprocessors.markdown import Markdown


class MarkdownTest(unittest.TestCase):

    def test_to_text(self):
        doc = '# Title'
        text = Markdown.markdown_to_plaintext(doc)
        self.assertEquals('Title', text)
