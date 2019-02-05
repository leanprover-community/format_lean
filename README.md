# Lean formatter

This prototype is a python library which renders convert Lean files to
other files, for instance another Lean file of a html file.

## Installation

You need Python 3.7 or later, and Lean. Make sure the python package
manager `pip` is installed.  Clone this repository, go to its root directory
and run `pip install .` (using `sudo` if needed). It's also recommended to
install `ipython` for interactive use. Alternatively, if you don't want to mess
up with your global python environment, you can use a dedicated virtual
environment, as explained below.

### Optional: setting up a virtual python environment
Use `pip install --user virtualenvwrapper`, and add to your `.bashrc` something like:
```bash
# Python virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
source $HOME/.local/bin/virtualenvwrapper.sh
```
You can then run `mkvirtualenv --python=/usr/bin/python3.7 format_lean` to
create your virtual environment. Once inside this environment (either because
you just created it or after running `workon format_lean`), you can pip
install. Note that you can leave the environment by running `deactivate`.


## Usage

If you only want to play with my example formatter in `lecture.py`,
you can fire ipython, `from format_lean.lecture import render_lean_file`
and then use 
`render_lean_file('my_file.lean', toolchain='3.4.2', lib_path='/usr/lib/lean-mathlib/src')`. Of course you need to point to your local copy of `mathlib` (unless you don't need mathlib?!). You can omit `toolchain` if you don't use `elan` (but why would you do that?!). Optional arguments also include `outpath` if replacing `.lean` by `.html` is not good enough, and `templates` if you want to point to an alternate template directory.
