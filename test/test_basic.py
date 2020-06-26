import pytest
from format_lean.cli.format_lean import render_lean_file

class TestBasic:
    def test_sandwich_render(self):
        render_lean_file("examples/src/sandwich.lean")
      

