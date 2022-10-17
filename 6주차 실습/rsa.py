# BigNumber, mpmath package required
# run this before execute: pip install BigNumber mpmath
# import math for gcd func
import random
import math
from BigNumber import BigNumber

# https://www.delftstack.com/howto/python/python-generate-prime-number/
def primesInRange(x, y):
    prime_list = []
    for n in range(x, y):
        isPrime = True

        for num in range(2, n):
            if n % num == 0:
                isPrime = False

        if isPrime:
            prime_list.append(n)
            
    return prime_list

def make_keys(p: BigNumber, q: BigNumber):
    # place your own implementation of make_keys
    # use e = 65537 as if FIPS standard
    n = p*q
    p_n = (p-1) * (q-1)
    e = 65537
    while math.gcd(p_n, e) != 1:
        pass
    d = 1
    while (e*d) % p_n != 1 or d == e:
        d = d+1
    

    return [e, d, n]

def rsa_encrypt(plain: BigNumber, e: BigNumber, n: BigNumber):
    # place your own implementation of rsa_encrypt
    c = (plain**e) % n
    return c

def rsa_decrypt(cipher: BigNumber, d: BigNumber, n: BigNumber):
    # place your own implementation of rsa_decrypt
    m = (cipher**d) % n
    return m

primes = primesInRange(100, 1000)

P = primes[random.randrange(0, len(primes))]
Q = primes[random.randrange(0, len(primes))]

while P == Q:
    P = primes[random.randrange(0, len(primes))]
    Q = primes[random.randrange(0, len(primes))]

M = random.randrange(2, 20)
e, d, N = make_keys(P, Q)
C = rsa_encrypt(M, e, N)
M2 = rsa_decrypt(C, d, N)

print(f"P = {P}, Q = {Q}, N = {N}, M = {M}, e = {e}, d = {d}, C = {C}, M2 = {M2}")

if M == M2:
    print("RSA Success!!")
else:
    print("RSA Failed...")
