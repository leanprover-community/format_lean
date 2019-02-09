from pathlib import Path
import os, shutil

from format_lean.line_reader import FileReader
from format_lean.renderer import Renderer
from format_lean.objects import (HeaderBegin, HeaderEnd, SectionBegin,
    SectionEnd, SubSectionBegin, SubSectionEnd, TextBegin, TextEnd,
    DefinitionBegin, DefinitionEnd, LemmaBegin, LemmaEnd, ProofBegin, ProofEnd,
    ProofComment)

def render_lean_file(inpath, outpath=None, outdir=None,
        toolchain=None, lib_path=None, templates=None):
    if toolchain:
        lean_exec_path = Path.home() / '.elan/toolchains' / toolchain / 'bin/lean'
    else:
        lean_exec_path = Path(distutils.spawn.find_executable('lean'))
    core_path = lean_exec_path.parent / '../lib/lean/library'
    lean_path = f'{core_path}:{lib_path}' if lib_path else core_path
    templates = templates or str(Path(__file__).parent / '../../templates/')

    outpath = outpath or inpath.replace('.lean', '.html')

    if outdir:
        if not Path(outdir).is_dir():
            os.makedirs(outdir)
        outpath = str(Path(outdir) / outpath)
        for path in (Path(__file__).parent / '../../').glob('*.css'):
            shutil.copy(path, outdir)
        for path in (Path(__file__).parent / '../../').glob('*.js'):
            shutil.copy(path, outdir)

    lecture_reader = FileReader(lean_exec_path, lean_path, 
            [HeaderBegin, HeaderEnd, SectionBegin, SectionEnd, SubSectionBegin,
             SubSectionEnd, TextBegin, TextEnd, DefinitionBegin,
             DefinitionEnd, LemmaBegin, LemmaEnd, ProofBegin, ProofEnd,
             ProofComment])
    lecture_reader.read_file(inpath)
    renderer = Renderer.from_file(templates)
    renderer.render(lecture_reader.output, outpath)

