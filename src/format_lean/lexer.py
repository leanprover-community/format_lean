"""
    pygments.lexers.theorem
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for theorem-proving languages.

    :copyright: Copyright 2006-2022 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import RegexLexer, default, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Generic

__all__ = ['LeanLexer']


class LeanLexer(RegexLexer):
    """
    For the Lean theorem prover.

    .. versionadded:: 2.0
    """
    name = 'Lean'
    url = 'https://github.com/leanprover/lean'
    aliases = ['lean']
    filenames = ['*.lean']
    mimetypes = ['text/x-lean']

    tokens = {
        'root': [
            (r'\s+', Text),
            (r'/--', String.Doc, 'docstring'),
            (r'/-', Comment, 'comment'),
            (r'--.*?$', Comment.Single),
            (words((
                'import', 'renaming', 'hiding',
                'namespace',
                'local',
                'private', 'protected', 'section',
                'include', 'omit', 'section',
                'protected', 'export',
                'open',
                'attribute',
            ), prefix=r'\b', suffix=r'\b'), Keyword.Namespace),
            (words((
                'lemma', 'theorem', 'def', 'definition', 'example',
                'axiom', 'axioms', 'constant', 'constants',
                'universe', 'universes',
                'inductive', 'coinductive', 'structure', 'extends',
                'class', 'instance',
                'abbreviation',

                'noncomputable theory',

                'noncomputable', 'mutual', 'meta',

                'attribute',

                'parameter', 'parameters',
                'variable', 'variables',

                'reserve', 'precedence',
                'postfix', 'prefix', 'notation', 'infix', 'infixl', 'infixr',

                'begin', 'by', 'end',

                'set_option',
                'run_cmd',
            ), prefix=r'\b', suffix=r'\b'), Keyword.Declaration),
            (r'@\[[^\]]*\]', Keyword.Declaration),
            (words((
                'forall', 'fun', 'Pi', 'from', 'have', 'show', 'assume', 'suffices',
                'let', 'if', 'else', 'then', 'in', 'with', 'calc', 'match',
                'do',
                "On", "Montrons", "Fait", "Par", "Posons", "Soit", "Supposons", "applique", "appliqué", "à", "on", "obtient", "choisit", "que", "tel", "convient", "une", "contradiction", "conclut", "par", "calcule", "dans", "combine", "réécrit", "via", "partout", "contrapose", "simplement", "discute", "selon", "il", "suffit", "de", "montrer", "déplie", "l'absurde", "renomme", "en", "oublie", "reformule", "récurrence", "pousse", "la", "négation", "utilisant", "qui", "devient"
            ), prefix=r'\b', suffix=r'\b'), Keyword),
            (words(('sorry', 'admit'), prefix=r'\b', suffix=r'\b'), Generic.Error),
            (words(('Sort', 'Prop', 'Type'), prefix=r'\b', suffix=r'\b'), Keyword.Type),
            (words((
                '#eval', '#check', '#reduce', '#exit',
                '#print', '#help',
            ), suffix=r'\b'), Keyword),
            (words((
                '(', ')', ':', '{', '}', '[', ']', '⟨', '⟩', '‹', '›', '⦃', '⦄', ':=', ',',
            )), Operator),
            (r'[A-Za-z_\u03b1-\u03ba\u03bc-\u03fb\u1f00-\u1ffe\u2100-\u214f]'
             r'[.A-Za-z_\'\u03b1-\u03ba\u03bc-\u03fb\u1f00-\u1ffe\u2070-\u2079'
             r'\u207f-\u2089\u2090-\u209c\u2100-\u214f0-9]*', Name),
            (r'0x[A-Za-z0-9]+', Number.Integer),
            (r'0b[01]+', Number.Integer),
            (r'\d+', Number.Integer),
            (r'"', String.Double, 'string'),
            (r"'(?:(\\[\\\"'nt])|(\\x[0-9a-fA-F]{2})|(\\u[0-9a-fA-F]{4})|.)'", String.Char),
            (r'[~?][a-z][\w\']*:', Name.Variable),
            (r'\S', Name.Builtin.Pseudo),
        ],
        'comment': [
            (r'[^/-]', Comment.Multiline),
            (r'/-', Comment.Multiline, '#push'),
            (r'-/', Comment.Multiline, '#pop'),
            (r'[/-]', Comment.Multiline)
        ],
        'docstring': [
            (r'[^/-]', String.Doc),
            (r'-/', String.Doc, '#pop'),
            (r'[/-]', String.Doc)
        ],
        'string': [
            (r'[^\\"]+', String.Double),
            (r"(?:(\\[\\\"'nt])|(\\x[0-9a-fA-F]{2})|(\\u[0-9a-fA-F]{4}))", String.Escape),
            ('"', String.Double, '#pop'),
        ],
    }
