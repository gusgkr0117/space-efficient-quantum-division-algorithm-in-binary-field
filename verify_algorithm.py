import random
from math import floor, log

n = 571

def bitReverse(num, nbit):
    b = '{:0{width}b}'.format(num, width=nbit)
    return int(b[::-1], 2)


def leftRotate(m, nbit):
    b = (m & 1)
    m = (m >> 1) | (b << (nbit-1))
    return m


def bitMult(a, b):
    c = 0
    while a.bit_length() > 0:
        if (a&1)==1: c ^= b
        b <<= 1
        a >>= 1
    return c

def modular(n, m):
    while n.bit_length() >= m.bit_length():
        n ^= (m << (n.bit_length() - m.bit_length()))
    return n


def CTOF_with_unary_iteration(mask, q, a, b, ell):   # mask, g[0], f, g
    # Lambda = n - 1 - max(floor((ell-1)/2), 0)
    t = 0                                                           # t <- 0
    for i in range(max(floor((ell-1)/2), 0), n):                    # unary iteration
        if mask == i and q == 1 and i <= min(ell, n-1):             # unary iteration only for max(floor((ell-1)/2), 0) <= i <= min(ell, n-1)
            t ^= 1                                                  # t <- TOF(t, unary_iteration_i(mask), q)

        if t == 1 and i != n - 1:                                   # skip the last part
            b ^= a & (1 << (n - i - 1))                             # g[Lambda - i - 1] <- TOF(g[Lambda - i - 1], t, f[Lambda - i - 1])

    t ^= q                                                          # t <- CNOT(t, q)
    assert(t == 0)
    return b

for k in range(1000):
    R_0 = (1<<571) | (1<<10) | (1<<5) | (1<<2) | 1
    # R_1 = (1<<7) | (1<<4) | 1
    R_1 = 0
    while R_1 == 0:
        for i in range(n): R_1 ^= (random.randint(0,1)<<i)
    
    f = bitReverse(R_0, n + 1)
    g = bitReverse(R_1, n)
    v, r = 0, 1
    delta = 1
    mask = 0

    a, b = 0, 0
    for i in range(2*n - 1):
        v <<= 1                                     # v <- RIGHTSHIFT(v)
        a ^= (delta > 0) & ((g&1)==1)               # a <- TOF(sign, g[0], a)
        b ^= (delta > 0) & ((g&1)==0)               # b <- TOF(sign, g[0] + 1, b)

        if a :
            f, g = g, f                             # f, g <- CSWAP_a(f[n...0],g[n...0])
            v, r = r, v                             # v, r <- CSWAP_a(v[lambda...0],r[lambda...0])

        g = CTOF_with_unary_iteration(mask, (g&1), f, g, i)  # g[Lambda...1] <- CTOF_WITH_UNARY_ITERATION_i(mask, g[0], f[Lambda...1], g[Lambda...1])

        if b : mask += 1                             # mask <- INC_b(mask)
        b ^= (delta > 0) & ((g&1)==0)               # b <- TOF(sign, g[0] + 1, b)

        if (delta==0) : mask += 1                    # mask <- C^n-INC_delta(mask)

        if a : delta = 1- delta                     # delta <- CNOT(a, delta)
        else: delta = 1 + delta                     # delta <- INC_(1+a)(delta)
        
        a ^= ((g&1)==1) & ((v&1)==1)                # a <- TOF(v[0], g[0], a)

        if (g&1)==1:
            r = r ^ v                               # r <- TOF(g[0], v[lambda...0], r[lambda...0])

        g = leftRotate(g, n+1)                      # g <- LEFTROTATE(g[n...0])

        assert(max(r.bit_length(), v.bit_length()) <= min(i, n) + 1) # lambda
        assert(mask >= max(floor((i-1)/2), 0)) # Lambda
        assert(a==0 & b==0)

    inv_R_1 = bitReverse(v, n)
    result = modular(bitMult(inv_R_1, R_1), R_0)
    assert(result == 1)

print("succeed")