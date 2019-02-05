from dataclasses import dataclass, field
from copy import copy

from jinja2 import Environment, FileSystemLoader

from pygments.lexers import LeanLexer
from pygments import highlight 
from pygments.formatters import HtmlFormatter


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

    def render(self, objects, out_path):
        """
        Renders objects to path
        """
        res = '\n'.join([
            self.env.get_template(obj.name).render(obj=color(obj)) for obj in objects])
        self.env.get_template('page').stream({ 'title': 'Lean test', 'content':
            res}).dump(out_path)

    @classmethod
    def from_file(cls, path):
        return cls(
                env=Environment(loader=FileSystemLoader(path)))



