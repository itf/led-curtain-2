'''
Pattern builders are functions that take 0
or more arguments and return a pattern
'''
import Patterns.Pattern as P
import Patterns.StaticPatterns.basicPatterns as bP
import copy

def cached(pattern):
    cache = [None]
    @wraps(pattern)
    def cached_f(patternInput):
        if cache[0]==None:
            cache[0] = pattern(patternInput)
        return copy.copy(cache[0])
    return cached_f

def constantBuilder():
    myOutput=None
    def constant(patternInput):
        
