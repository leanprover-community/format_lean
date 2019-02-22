from dataclasses import dataclass, field
from typing import List
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
    ts_filters: List =  field(default_factory=list)

    def transform_text(self, text):
        return Text(paragraphs=[
            Paragraph(content=self.markdown_renderer.render(Document(par.content)))
            for par in text.paragraphs])

    def transform_theorem(self, theorem):
        for proof_item in theorem.proof.items:
            for proof_line in proof_item.lines:
                for r, s in self.ts_filters:
                    proof_line.tactic_state_left = r.sub(
                            s, proof_line.tactic_state_left)
                    proof_line.tactic_state_right = r.sub(
                            s, proof_line.tactic_state_right)
        return theorem

    def render(self, objects, out_path, page_context=None, title=None):
        """
        Renders objects to path
        """
        objects = [getattr(self, f'transform_{obj.name}', lambda x: x)(obj)
                   for obj in objects]
        page_context = page_context or dict()
        page_context['title'] = page_context.get('title', title or 'Lean')
        res = '\n'.join([
            self.env.get_template(obj.name).render(obj=color(obj),
                lang=page_context['lang']) for obj in objects])
        page_context['content'] = res
        self.env.get_template('page').stream(page_context).dump(out_path)

    @classmethod
    def from_file(cls, path, ts_filters=None):
        return cls(
                env=Environment(loader=FileSystemLoader(path)), ts_filters=ts_filters)

