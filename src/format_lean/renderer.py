from dataclasses import dataclass, field
from copy import copy

from jinja2 import Environment, FileSystemLoader
from mistletoe.html_renderer import HTMLRenderer
from mistletoe.block_token import Document

from pygments.lexers import LeanLexer
from pygments import highlight 
from pygments.formatters import HtmlFormatter

from format_lean.objects import Text, Paragraph

lexer = LeanLexer(leanstripall=True)    
formatter = HtmlFormatter(linenos=False) 

def color(obj):
    if hasattr(obj, 'lean'):
        obj.lean = highlight(obj.lean, lexer, formatter)
    if hasattr(obj, 'proof'):
        for proof_item in obj.proof.items:
            for line in proof_item.lines:
                line.lean = highlight(line.lean, lexer, formatter)
                line.tactic_state_left = highlight(line.tactic_state_left, lexer, formatter)
                line.tactic_state_right = highlight(line.tactic_state_right, lexer, formatter)
    return obj


@dataclass
class Renderer:
    env: Environment = None
    markdown_renderer: HTMLRenderer = field(default_factory=HTMLRenderer)

    def render_text(self, text):
        return Text(paragraphs=[
            Paragraph(content=self.markdown_renderer.render(Document(par.content)))
            for par in text.paragraphs])

    def render(self, objects, out_path):
        """
        Renders objects to path
        """
        objects = [self.render_text(obj) if obj.name == 'text' else obj 
                   for obj in objects]
        res = '\n'.join([
            self.env.get_template(obj.name).render(obj=color(obj)) for obj in objects])
        self.env.get_template('page').stream({ 'title': 'Lean test', 'content':
            res}).dump(out_path)

    @classmethod
    def from_file(cls, path):
        return cls(
                env=Environment(loader=FileSystemLoader(path)))



