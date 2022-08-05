from sage.all import *

# n = 571

R.<n,logn> = PolynomialRing(QQ)

sum_1 = 2*n - 1
sum_Lambda = n^2 - 1
sum_lambda = 3/2*n^2 - 3/2*n

TOF = 0
CNOT = 0

# for i in range(2*n - 1):
CNOT += 0                                   # v <- RIGHTSHIFT(v)
TOF += 1 * sum_1                            # a <- TOF(sign, g[0], a)
TOF += 1 * sum_1                            # b <- TOF(sign, g[0] + 1, b)

CNOT += 2*n * sum_1                         # f, g <- CSWAP_a(f[n...0],g[n...0])
TOF += n * sum_1

CNOT += 2 * sum_lambda                      # v, r <- CSWAP_a(v[lambda...0],r[lambda...0])
TOF += sum_lambda


TOF += 3 * sum_Lambda                       # g[n...1] <- CTOF(g[0], f[Lambda...1], mask[Lambda...1], g[Lambda...1])

CNOT += 2 * sum_Lambda                      # mask <- LEFTSHIFT_b(mask)
TOF += sum_1 + sum_Lambda           

TOF += 1 * sum_1                            # b <- TOF(sign, g[0] + 1, b)

CNOT += 2 * sum_Lambda                      # mask <- C^n-LEFTSHIFT_delta(mask)
TOF += (4 * logn - 2) * sum_1 + sum_Lambda

CNOT += sum_1                               # delta <- CNOT(a, delta)

CNOT += (2*logn + 3) * sum_1                # delta <- INC_(1+a)(delta)
TOF += (22*logn + 26) * sum_1

TOF += sum_1                                # a <- TOF(v[0], g[0], a)

TOF += sum_lambda + sum_1                   # r <- TOF(g[0], v[lambda...0], r[lambda...0])

CNOT += 0                                   # g <- LEFTROTATE(g[n...0])

print("TOF :", TOF * 2)
print("CNOT :", CNOT * 2)

############## Original Resource Measurement ###############

sum_1 = 2*n - 1
sum_Lambda = 3/2*n^2 - 3/2*n
sum_lambda = 3/2*n^2 - 1/2*n

TOF = 0
CNOT = 0

# for i in range(2*n - 1):
CNOT += 0                                   # v <- RIGHTSHIFT(v)
TOF += 1 * sum_1                            # a <- TOF(sign, g[0], a)
CNOT += (logn + 2) * sum_1                  # delta <- CNOT(delta, a)

CNOT += 2 * sum_Lambda                      # f, g <- CSWAP_a(f[Lambda...0],g[Lambda...0])
TOF += sum_Lambda 

CNOT += 2 * sum_lambda                      # v, r <- CSWAP_a(v[lambda...0],r[lambda...0])
TOF += sum_lambda

CNOT += (2*logn + 3) * sum_1                # delta <- INC_(1+a)(delta)
TOF += (22*logn + 26) * sum_1


CNOT += sum_1                               # a <- CNOT(a,v[0])

CNOT += sum_1                               # g_0[l] <- CNOT(g[0], g_0[l])

TOF += sum_Lambda + sum_1                   # g <- TOF(g_0[l], f[Lambda...0], g[Lambda...0])
TOF += sum_lambda + sum_1                   # r <- TOF(g_0[l], v[lambda...0], r[lambda...0])

CNOT += 0                                   # g <- LEFTSHIFT(g[n...0])

print("TOF :", TOF * 2)
print("CNOT :", CNOT * 2)