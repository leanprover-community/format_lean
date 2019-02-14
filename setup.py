from setuptools import setup, find_packages

setup(
    name='Lean formatter',
    version='0.0.2',
    author='Patrick Massot',
    author_email='patrickmassot@free.fr',
    description='A Lean prover text formatter',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={
        '': ['*.css', '*.css.map', '*.js', 'templates/*'],
    },
    scripts=['bin/format_lean', 'bin/format_project'],
    install_requires=['regex >= 2018.7.11', 'jinja2 >= 2.10', 'mistletoe >= 0.7.1', 'toml >= 0.10.0', 'fire >= 0.1.3'])
