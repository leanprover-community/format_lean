import os
from pathlib import Path
import pytest
from format_lean.cli.format_lean import render_lean_file
from format_lean.cli.format_project import render_lean_project

class TestBasic:
    def test_sandwich_render(self):
        render_lean_file("examples/src/sandwich.lean", lib_path="examples/_target/deps/mathlib/src", debug=True)
    # def test_sandwich_project_render(self):
    #     os.chdir(Path.cwd().parent/"examples")
    #     render_lean_project(debug=True)
      

