from setuptools import setup, find_packages

setup(
    name='format_lean',
    version='0.0.2',
    author='Patrick Massot',
    author_email='patrickmassot@free.fr',
    description='A Lean prover text formatter',
    packages=find_packages(),
    package_data={
        '': ['*.css', '*.css.map', '*.js', 'templates/*'],
    },
    entry_points = {
        "console_scripts": [
            'format_lean = format_lean.cli.format_lean:main',
            'format_project = format_lean.cli.format_project:main'
        ],
    },
    install_requires=['regex==2019.11.1', 'jinja2 >= 2.10',
                      'mistletoe >= 0.7.1', 'toml >= 0.10.0',
                      'fire >= 0.1.3', 'beautifulsoup4 >= 4.7.1', "pygments>=2.6.1"])
