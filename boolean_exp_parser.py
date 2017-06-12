# ---------------
# User Instructions
#
# In this problem, you will be using many of the tools and techniques
# that you developed in unit 3 to write a grammar that will allow
# us to write a parser for the JSON language.
#
# You will have to visit json.org to see the JSON grammar. It is not
# presented in the correct format for our grammar function, so you
# will need to translate it.

# ---------------
# Provided functions
#
# These are all functions that were built in unit 3. They will help
# you as you write the grammar.  Add your code at line 102.

from functools import update_wrapper
from string import split
import re

def grammar(description, whitespace=r'\s*'):
    """Convert a description to a grammar.  Each line is a rule for a
    non-terminal symbol; it looks like this:
        Symbol =>  A1 A2 ... | B1 B2 ... | C1 C2 ...
    where the right-hand side is one or more alternatives, separated by
    the '|' sign.  Each alternative is a sequence of atoms, separated by
    spaces.  An atom is either a symbol on some left-hand side, or it is
    a regular expression that will be passed to re.match to match a token.

    Notation for *, +, or ? not allowed in a rule alternative (but ok
    within a token). Use '\' to continue long lines.  You must include spaces
    or tabs around '=>' and '|'. That's within the grammar description itself.
    The grammar that gets defined allows whitespace between tokens by default;
    specify '' as the second argument to grammar() to disallow this (or supply
    any regular expression to describe allowable whitespace between tokens)."""
    G = {' ': whitespace}
    description = description.replace('\t', ' ') # no tabs!
    for line in split(description, '\n'):
        lhs, rhs = split(line, ' => ', 1)
        alternatives = split(rhs, ' | ')
        G[lhs] = tuple(map(split, alternatives))
    return G

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)
    return _f

def parse(start_symbol, text, grammar):
    """Example call: parse('Exp', '3*x + b', G).
    Returns a (tree, remainder) pair. If remainder is '', it parsed the whole
    string. Failure iff remainder is None. This is a deterministic PEG parser,
    so rule order (left-to-right) matters. Do 'E => T op E | T', putting the
    longest parse first; don't do 'E => T | T op E'
    Also, no left recursion allowed: don't do 'E => E op T'"""

    tokenizer = grammar[' '] + '(%s)'

    def parse_sequence(sequence, text):
        result = []
        for atom in sequence:
            tree, text = parse_atom(atom, text)
            if text is None: return Fail
            result.append(tree)
        return result, text

    @memo
    def parse_atom(atom, text):
        if atom in grammar:  # Non-Terminal: tuple of alternatives
            for alternative in grammar[atom]:
                tree, rem = parse_sequence(alternative, text)
                if rem is not None: return [atom]+tree, rem
            return Fail
        else:  # Terminal: match characters against start of text
            m = re.match(tokenizer % atom, text)
            return Fail if (not m) else (m.group(1), text[m.end():])

    # Body of parse:
    return parse_atom(start_symbol, text)

Fail = (None, None)

BOOLEAN_EXP = grammar("""exp => term OR exp | term
term => word AND word | word
word => not factor | factor
factor => var | [(] exp [)]
var => [a-zA-Z][a-zA-Z0-9]*
OR => or
AND => and""")

#print BOOLEAN_EXP

#print parse('exp', 'a and b', BOOLEAN_EXP)
#print parse('exp', 'var1 or var2', BOOLEAN_EXP)
#print parse('exp', 'a and b or c', BOOLEAN_EXP)
#print parse('exp', 'a or b and c', BOOLEAN_EXP)

# tree1, reminder1 =  parse('exp', '(a or b) and c', BOOLEAN_EXP)
# print tree1[0]
# print tree1[1]
# print len(tree1[1])
# for node in tree1[1]:
#     print node

# tree, reminder = parse('exp', 'a or b and c', BOOLEAN_EXP)
#
# for node in tree:
#     print node


############################################################################
# grammar specific code to deal with the parsed syntax tree

def evaluate_expression_tree(tree_in, environment):
    def exp(tree):
        if len(tree) == 4:
            return (term(tree[1]) or exp(tree[3]))
        elif len(tree) == 2:
            return term(tree[1])
        else:
            raise StandardError("exp evaluation failed. ")
            return False

    def term(tree):
        if len(tree) == 4:
            return (word(tree[1]) and word(tree[3]))
        elif len(tree) == 2:
            return word(tree[1])
        else:
            raise StandardError("term evaluation failed. ")
            return False

    def word(tree):
        if len(tree) == 3:
            return not factor(tree[2])
        elif len(tree) == 2:
            return factor(tree[1])
        else:
            raise StandardError("word evaluation failed. ")
            return False

    def factor(tree):
        if len(tree) == 2:
            value = False
            try:
                value = environment[tree[1][1]]
            except KeyError:
                raise StandardError("variable %s is not defined.", tree[1][1])
            return value
        elif len(tree) == 4:
            return exp(tree[2])
        else:
            raise StandardError("factor evaluation failed. ")
            return False

    return exp(tree_in)

tree_0, remainder_0 = parse('exp', 'a and b', BOOLEAN_EXP)
print tree_0
env_0 = {'a':True, 'b':True}
print evaluate_expression_tree(tree_0, env_0)

tree_1, reminder_1 =  parse('exp', '(a or b) and c', BOOLEAN_EXP)
print tree_1
env_1 = {'a': False, 'b':False, 'c': True}
print evaluate_expression_tree(tree_1, env_1)

tree_2, reminder_2 =  parse('exp', 'not (a or b) and not c', BOOLEAN_EXP)
print tree_2
env_2 = {'a': False, 'b':False, 'c': False}
print evaluate_expression_tree(tree_2, env_2)
