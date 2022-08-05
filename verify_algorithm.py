import random
import math

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
    mask = (1<<(n)) - 1

    #print(">>>Initial<<<")
    #print('f : {:0{width}b}'.format(f, width=n+1))
    #print('g : {:0{width}b}'.format(g, width=n+1))
    #print("=============")
    a, b = 0, 0
    for i in range(2*n - 1):
        v <<= 1 # v <- RIGHTSHIFT(v)
        a ^= (delta > 0) & ((g&1)==1)               # a <- TOF(sign, g[0], a)
        b ^= (delta > 0) & ((g&1)==0)               # b <- TOF(sign, g[0] + 1, b)

        if a :
            f, g = g, f                             # f, g <- CSWAP_a(f[n...0],g[n...0])
            v, r = r, v                             # v, r <- CSWAP_a(v[lambda...0],r[lambda...0])

        if (g&1)==1:
            g = g ^ (((f & mask) >> 1) << 1)        # g[n...1] <- CTOF(g[0], f[Lambda...1], mask[Lambda...1], g[Lambda...1])

        if b : mask >>= 1                           # mask <- LEFTSHIFT_b(mask)
        b ^= (delta > 0) & ((g&1)==0)               # b <- TOF(sign, g[0] + 1, b)

        if (delta==0) : mask >>= 1                  # mask <- C^n-LEFTSHIFT_delta(mask)

        if a : delta = 1- delta                     # delta <- CNOT(a, delta)
        else: delta = 1 + delta                     # delta <- INC_(1+a)(delta)
        
        a ^= ((g&1)==1) & ((v&1)==1)                # a <- TOF(v[0], g[0], a)

        if (g&1)==1:
            r = r ^ v                               # r <- TOF(g[0], v[lambda...0], r[lambda...0])

        g = leftRotate(g, n+1)                      # g <- LEFTROTATE(g[n...0])

        assert(max(r.bit_length(), v.bit_length()) <= min(i, n) + 1) # lambda
        assert(mask.bit_length() <= n - max(math.floor((i-1)/2), 0)) # Lambda
        assert(a==0 & b==0)
        #overlap = math.floor(n/2)
        #test = mask | (bitReverse(r, n+1) << (n - overlap))
        #print('a, b = %d %d'%(a,b))
        #print('test : {:0{width}b}'.format(test, width=2*n + 1 - overlap))
        #print(test.bit_length())
        #print('r : {:0{width}b}'.format(r, width=n+1))
        #print('m : {:0{width}b}'.format(mask, width=n+1))
        #input()

    #print('f : {:0{width}b}'.format(f, width=n+1))
    #print('g : {:0{width}b}'.format(g, width=n+1))
    #print('v : {:0{width}b}'.format(v, width=n+1))
    #print('r : {:0{width}b}'.format(r, width=n+1))
    #print("mask :", bin(mask))
    #print('delta :', delta)

    inv_R_1 = bitReverse(v, n)
    #print('inv_R_1 : {:0{width}b}'.format(inv_R_1, width=n+1))
    result = modular(bitMult(inv_R_1, R_1), R_0)
    assert(result == 1)

print("succeed")