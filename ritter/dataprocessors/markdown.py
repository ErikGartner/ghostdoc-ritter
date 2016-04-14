from bs4 import BeautifulSoup
from markdown import markdown


class Markdown():

    def markdown_to_plaintext(markdown_text):
        html = markdown(markdown_text)
        text = ''.join(BeautifulSoup(html, 'html.parser').findAll(text=True))
        return text

    def tree_to_plaintext(marked_tree):
        text_list = []
        for item in marked_tree:
            if 'text' in item:
                text_list.append(item['text'])
        return '\n'.join(text_list)
