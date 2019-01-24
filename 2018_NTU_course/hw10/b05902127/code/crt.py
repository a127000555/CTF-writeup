# https://gist.github.com/ikautak/5541975
def xeuclid(a, b):
    """ return gcd(a,b), x and y in 'gcd(a,b) = ax + by'.
    """
    x = [1, 0]
    y = [0, 1]
    sign = 1

    while b:
        q, r = divmod(a, b)
        a, b = b, r
        x[1], x[0] = q*x[1] + x[0], x[1]
        y[1], y[0] = q*y[1] + y[0], y[1]
        sign = -sign

    x = sign * x[0]
    y = -sign * y[0]
    return a, x, y
from functools import reduce

def crt(a, m):
    """ return x in ' x = a mod m'.
    """
    modulus = reduce(lambda a,b: a*b, m)

    multipliers = []
    for m_i in m:
        M = modulus // m_i
        gcd, inverse, y = xeuclid(M, m_i)
        multipliers.append(inverse * M % modulus)

    result = 0
    for multi, a_i in zip(multipliers, a):
        result = (result + multi * a_i) % modulus
    return result