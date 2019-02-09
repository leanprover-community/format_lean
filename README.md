# Lean formatter

This prototype is a python library which renders convert Lean files to
other files, for instance another Lean file of a html file.

## Installation

You need Python 3.7 or later, and Lean. Make sure the python package
manager `pip` is installed.  Clone this repository, go to its root directory
and run `pip install .` (using `sudo -H` if needed). It's also recommended to
install `ipython` for interactive use. Alternatively, if you don't want to mess
up with your global python environment, you can use a dedicated virtual
environment. This is explained in the more complete 
[installation guide](https://github.com/leanprover-community/format_lean/blob/master/INSTALL.md).

## Usage

If you only want to play with my example formatter in `lecture.py`,
you can fire ipython, `from format_lean.lecture import render_lean_file`
and then use 
`render_lean_file('my_file.lean', toolchain='3.4.2', lib_path='/usr/lib/lean-mathlib/src')`. Of course you need to point to your local copy of `mathlib` (unless you don't need mathlib?!). You can omit `toolchain` if you don't use `elan` (but why would you do that?!). Optional arguments also include `outpath` if replacing `.lean` by `.html` is not good enough, and `templates` if you want to point to an alternate template directory.
