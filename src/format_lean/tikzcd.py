import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from bs4 import BeautifulSoup

from mistletoe import HTMLRenderer
from jinja2 import Template

import format_lean

module_path = Path(format_lean.__file__).parent

class TikzcdRenderer(HTMLRenderer):
    def __init__(self, *args, **kwargs):
        
        if 'tikzcd-tpl' in kwargs:
            tpl = kwargs.pop('tikzcd-tpl')
        else:
            tpl = str(module_path / 'templates' / 'tikzcd')
        with open(tpl, "r") as file:
            self.tikzcd_tpl = Template(file.read())
        self.tikz_scale = kwargs.pop('tikz_scale', 1.5)
        return super().__init__(*args, **kwargs)

    def render_block_code(self, token):
        if token.language == 'cd':
            code = token.children[0].content
            with TemporaryDirectory() as name:
                tdir = Path(name)
                texpath = str(tdir / 'tmp.tex')
                pdfpath = str(tdir / 'tmp.pdf')
                svgpath = str(tdir / 'tmp.svg')
                self.tikzcd_tpl.stream(cd=code).dump(texpath)
                subprocess.call(['xelatex', '--output-dir', name, texpath])
                subprocess.call(['pdf2svg', pdfpath, svgpath])
                with open(svgpath) as f:
                    svg = BeautifulSoup(f, features="html.parser").svg
                svg['width'] = f'{self.tikz_scale*float(svg["width"][:-2])}pt'
                svg['height'] = f'{self.tikz_scale*float(svg["height"][:-2])}pt'
                return f'<div class="tikzcd">\n{svg}\n</div>\n'
        else:
            return super().render_block_code(token) 

