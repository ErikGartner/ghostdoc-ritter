from bs4 import BeautifulSoup
from markdown import markdown


class MarkdownMixin():

    def markdown_to_text(self, markdown_text):
        html = markdown(markdown_text)
        text = ''.join(BeautifulSoup(html, 'html.parser').findAll(text=True))
        return text
