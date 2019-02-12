# Lean formatter full install guide

This guide assumes you use a Debian-based Linux (e.g. Ubuntu), although
it may hopefully be somewhat relevant to more exotic operating systems.
It will install this software in an isolated environment. Of course this
means wasting some space, but it guarantees no unwanted side effects.

## Python 3.7

You need a recent python, at least python 3.7, because we use 
the [dataclass decorator](https://docs.python.org/3.7/library/dataclasses.html#module-dataclasses). An easy way to arrange that is to use [PyEnv](https://github.com/pyenv/pyenv).
```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```
You need to make sure your shell will find pyenv, for instance typing:
```bash
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
```

You are now ready to download python 3.7. It will be installed in your
home directory, but you still need some system-wide library support. A
good way to make sure everything is there is to run:
```bash
sudo apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl
```
or the equivalent command for non-Debian distributions.

Then restart a shell in order to get your new PATH variable (or use
`source ~/.bashrc`) and install the python version you need.
```bash
pyenv install 3.7.2
```
You should now have a working copy of python 3.7.2 hidden in
`$HOME/.pyenv/versions/3.7.2` (pyenv does not do anything outside of
this `.pyenv` folder, so you can very easily get rid of it by deleting
this folder, and unsetting the PATH variable addition).

We will now prepare for a virtual environment dedicated to
`format_lean`. The most convenient way is to use a system-wide
`virtualenvwrapper`, setting three shell environment variables to
configure it:
```bash
sudo apt install virtualenv python3-pip
sudo -H pip3 install virtualenvwrapper
echo -e 'export WORKON_HOME=$HOME/.virtualenvs\nexport VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3\nsource /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc
```
And then create a virtual environment for `format_lean` (after
restarting you shell, or at least sourcing bashrc in order to get those
variables set) typing in your home: 
```bash
mkvirtualenv --python=$HOME/.pyenv/versions/3.7.2/bin/python format_lean
```

## Install a custom pygment library

You will probably also want to get Lean syntax highlighthing. The most
up to date version of [pygment](http://pygments.org/) for Lean can be found in
[Gabriel's Ebner fork](https://bitbucket.org/gebner/pygments-main/downloads/)

Activate your python virtualenv by typing `workon format_lean` in case
you left it after creating it. Then download pygment using the above
link, uncompress it, go to the created folder and type `pip install .`.
You can then get rid of this folder.

## Install `format_lean`

Sill inside the virtual environment, type 
```bash
git clone https://github.com/leanprover-community/format_lean.git
cd format_lean
pip install .
```

You now have the format Lean library inside you virtual environment. You
probably also want to `pip install ipython` for a nicer interactive
experience.
