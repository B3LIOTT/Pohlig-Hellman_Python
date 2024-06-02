from math import gcd
from functools import reduce

def pollard_p_minus_1(n, B=10000):
    a = 2
    for j in range(2, B):
        a = pow(a, j, n)
        d = gcd(a - 1, n)
        if 1 < d < n:
            return d
        
    return None

def factorize_with_pollard(n):
    factors = {}
    while n > 1:
        factor = pollard_p_minus_1(n)
        if factor is None:
            factors[n] = 1
            break
        count = 0
        while n % factor == 0:
            n //= factor
            count += 1
        factors[factor] = count

    return [(q, r) for q, r in factors.items()]
