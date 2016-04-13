from bs4 import BeautifulSoup
from markdown import markdown


class Markdown():

    def markdown_to_plaintext(markdown_text):
        html = markdown(markdown_text)
        text = ''.join(BeautifulSoup(html, 'html.parser').findAll(text=True))
        return text
