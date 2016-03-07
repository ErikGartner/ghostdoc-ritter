import markdown
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension

class MarkdownCompiler:
    md = markdown.Markdown(extensions=[myext])

class RitterExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        md.treeprocessors.add('artifact_tagger', ArtifactTagger())

class ArtifactTagger(markdown.treeprocessors.Treeprocessor):

    def run(self, root):
        print(root)
