'''
Code to convert from the SRGB color profile to linear color profile
LEDs use the linear color profile, while, computer screens uses SRGB

This allows for a more accurate representation of colors on the LED panels.

Code adapted from James Bowman
Copyright 2009-2015 James Bowman. http://excamera.com/sphinx/article-srgb.html
Used with permission of the author
'''
import math

class Chebyshev:
    """
    Chebyshev(a, b, n, func)
    Given a function func, lower and upper limits of the interval [a,b],
    and maximum degree n, this class computes a Chebyshev approximation
    of the function.
    Method eval(x) yields the approximated function value.
    """
    def __init__(self, a, b, n, func):
        self.a = a
        self.b = b
        self.func = func

        bma = 0.5 * (b - a)
        bpa = 0.5 * (b + a)
        f = [func(math.cos(math.pi * (k + 0.5) / n) * bma + bpa) for k in range(n)]
        fac = 2.0 / n
        self.c = [fac * sum([f[k] * math.cos(math.pi * j * (k + 0.5) / n) for k in range(n)]) for j in range(n)]

    def eval(self, x):
        a,b = self.a, self.b
        assert(a <= x <= b)
        y = (2.0 * x - a - b) * (1.0 / (b - a))
        y2 = 2.0 * y
        (d, dd) = (self.c[-1], 0)             # Special case first step for efficiency
        for cj in self.c[-2:0:-1]:            # Clenshaw's recurrence
            (d, dd) = (y2 * d - dd + cj, d)
        return y * d - dd + 0.5 * self.c[0]   # Last step is different

__c_exp2__ = Chebyshev(0, 1, 4, lambda x: math.pow(2, x))
__c_log2__ = Chebyshev(0.5, 1, 4, lambda x: math.log(x) / math.log(2))

def exp2(x):
    xi = int(math.floor(x))
    xf = x - xi
    return math.ldexp(__c_exp2__.eval(xf), xi)

def log2(x):
    (xf, xi) = math.frexp(x)
    return xi + __c_log2__.eval(xf)

def pow(a, b):
    return exp2(b * log2(a))


def s2lin(x):
    a = 0.055
    if x <= 0.04045:
        return x * (1.0 / 12.92)
    else:
        return pow((x + a) * (1.0 / (1 + a)), 2.4)


def lin2s(x):
    a = 0.055
    if x <= 0.0031308:
        return x * 12.92
    else:
        return (1 + a) * pow(x, 1 / 2.4) - a
                 
####End of code by James Bowman.


def convertColorToLin(color, brightness):
    r,g,b = map(s2lin,color)
    r*=brightness
    g*=brightness
    b*=brightness
    return r,g,b

def convertColorToS(color):
    r,g,b = map(lin2s,color)
    return r,g,b

def convertColorByteToS(color):
    r,g,b = [c/255. for c in color]
    r,g,b=convertColorToS((r,g,b))
    return min(255,int(r*255)),min(255,int(g*255)),min(255,int(b*255))
