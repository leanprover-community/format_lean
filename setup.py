from setuptools import setup, find_packages

setup(
    name='Lean formatter',
    version='0.0.1',
    author='Patrick Massot',
    author_email='patrickmassot@free.fr',
    description='A Lean prover text formatter',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    scripts=['bin/format_lean'],
    install_requires=['regex >= 2018.7.11', 'jinja2 >= 2.10', 'mistletoe >= 0.7.1', 'toml >= 0.10.0'])
