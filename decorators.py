# test decorators

from functools import update_wrapper

def decorator(d):
    """Make a function d a decorator: d wrap a function fn"""
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def n_ary(f):
    """ given binary function f(x, y), return an n_ary
    function such that f(x, y, z) = f(x, f(y, z)).
    Also allow f(x) = x """
    def n_ary_f(x, *args):
        return x if not args else f(x, n_ary_f(*args))
    return n_ary_f

@n_ary
def add(x, y):
    """ return the sum of two values """
    return x + y

@decorator
def countcalls(f):
    """Decorator that makes the function count calls to it
    in callcounts[f]"""
    def _f(*args):
        callcounts[_f] += 1
        return f(*args)
    callcounts[_f] = 0
    return _f

callcounts = {}
