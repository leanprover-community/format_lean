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

If you only want to play with my example formatter you can simply run
`format_lean` (which should be in your path if `pip install .` did its
job). The basic usage is:
```bash
format_lean --inpath limits.lean --outdir build --lib-path /usr/lib/lean-mathlib/src
```
if you are in a folder containing `limits.lean`, have mathlib in `/usr/lib/lean-mathlib`, and 
want to render into directory `build`. See `format_lean -- --help` for
more option.

Of course you need to point to your local copy of `mathlib` (unless you
don't need mathlib?!). You can use `--toolchain` if your default `elan`
toolchain isn't appropriate (you do use [elan](https://github.com/Kha/elan), right?). Optional
arguments also include `outpath` if replacing `.lean` by `.html` is not
good enough, and `templates` if you want to point to an alternate
template directory. 

The script source in the `bin` folder of this repository is a good entry
point to understand how to customize more.

If you get addicted to it, and want to render a full Lean project, you
can go to the root of the project (the folder containing `leanpkg.toml`)
and run `format_project`. Optional arguments `--outdir my_dir` and
`--template` as above. There is no need to point out a toolchain or
dependencies since those are indicated in your `leanpkg.toml`.
If you want to exclude files `src/hide_me.lean` and `src/secret.lean`
from the rendering process, you can create a file `format.toml` next to
your `leanpkg.toml` containing `exclude = ['hide_me.lean', 'secret.lean']`.
