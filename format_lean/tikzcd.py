import subprocess
import re
from pathlib import Path
from tempfile import TemporaryDirectory
from bs4 import BeautifulSoup

from mistletoe import HTMLRenderer
from mistletoe import block_token 
from mistletoe.block_token import BlockToken, Heading, BlockCode, Quote, CodeFence, ThematicBreak, List, Table, Footnote, Paragraph, ListItem, HTMLBlock, span_token
from mistletoe.html_renderer import HTMLRenderer
from jinja2 import Template

import format_lean

module_path = Path(format_lean.__file__).parent

class DisplayMath(BlockToken):
    """
    We don't want markdown to mess with LaTeX displaymath block delimited by
    \[ and \], so we need a new block token class.
    """
    pattern = re.compile(r'^\s*\\\[')

    def __init__(self, lines):
        self.content = ''.join(lines)

    @classmethod
    def start(cls, line):
        return bool(cls.pattern.match(line))

    @staticmethod
    def read(lines):
        line_buffer = [next(lines)]
        for line in lines:
            if line.endswith(r'\]'):
                break
            line_buffer.append(line)
        return line_buffer


class ParagraphMath(Paragraph):
    """
    A replacement for mistletoe Paragraph block token class. I don't know how
    to extend it to fit DisplayMath, so let's copy-paste.
    """
    @classmethod
    def read(cls, lines):
        line_buffer = [next(lines)]
        next_line = lines.peek()
        while (next_line is not None
                and next_line.strip() != ''
                and not Heading.start(next_line)
                and not CodeFence.start(next_line)
                and not Quote.start(next_line)
                and not DisplayMath.start(next_line)):

            # check if next_line starts List
            list_pair = ListItem.parse_marker(next_line)
            if (len(next_line) - len(next_line.lstrip()) < 4
                    and list_pair is not None):
                prepend, leader = list_pair
                # non-empty list item
                if next_line[:prepend].endswith(' '):
                    # unordered list, or ordered list starting from 1
                    if not leader[:-1].isdigit() or leader[:-1] == '1':
                        break

            # check if next_line starts HTMLBlock other than type 7
            html_block = HTMLBlock.start(next_line)
            if html_block and html_block != 7:
                break

            # check if we see a setext underline
            if cls.parse_setext and cls.is_setext_heading(next_line):
                line_buffer.append(next(lines))
                return SetextHeading(line_buffer)

            # check if we have a ThematicBreak (has to be after setext)
            if ThematicBreak.start(next_line):
                break

            # no other tokens, we're good
            line_buffer.append(next(lines))
            next_line = lines.peek()
        return line_buffer


class TikzcdRenderer(HTMLRenderer):
    def __init__(self, *args, **kwargs):
        
        if 'tikzcd-tpl' in kwargs:
            tpl = kwargs.pop('tikzcd-tpl')
        else:
            tpl = str(module_path / 'templates' / 'tikzcd')
        with open(tpl, "r") as file:
            self.tikzcd_tpl = Template(file.read())
        self.tikz_scale = kwargs.pop('tikz_scale', 1.75)
        # Note the next line actually returns None, but changes state (arghh).
        res = super().__init__(*args, **kwargs)
        # The following 4 lines are a hugly hack to replace Paragraph
        # by ParagraphMath and use DisplayMath. The API here is awful,
        # modifying a private global variable.
        block_token.remove_token(Paragraph)
        block_token._token_types.append(ParagraphMath)
        block_token._token_types.insert(0, DisplayMath)
        self.render_map['DisplayMath'] = self.render_display_math
        self.render_map['ParagraphMath'] = self.render_paragraph
        return res

    def render_block_code(self, token):
        if token.language == 'cd':
            code = token.children[0].content
            print(code)
            with TemporaryDirectory() as name:
                tdir = Path(name)
                texpath = str(tdir / 'tmp.tex')
                pdfpath = str(tdir / 'tmp.pdf')
                svgpath = str(tdir / 'tmp.svg')
                self.tikzcd_tpl.stream(cd=code).dump(texpath)
                print(self.tikzcd_tpl.render(cd=code))
                subprocess.call(['xelatex', '--output-dir', name, texpath])
                subprocess.call(['pdf2svg', pdfpath, svgpath])
                with open(svgpath) as f:
                    svg_str = f.read()
                ident = hash(code)
                svg_str = svg_str.replace('glyph', str(ident)[:6])
                svg = BeautifulSoup(svg_str, features="html.parser").svg
                svg['width'] = f'{self.tikz_scale*float(svg["width"][:-2])}pt'
                svg['height'] = f'{self.tikz_scale*float(svg["height"][:-2])}pt'
                return f'<div class="tikzcd">\n{svg}\n</div>\n'
        else:
            return super().render_block_code(token) 

    def render_display_math(self, token):
        return '<p>\n' + token.content + '</p>\n'


