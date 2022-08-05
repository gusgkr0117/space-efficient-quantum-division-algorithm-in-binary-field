import math


items = [8, 16, 127, 163, 233, 283, 571]

# TOF_new : 20*n^2 + 104*n*logn + 120*n - 52*logn - 74

for n in items:
	r = 20 * n ** 2
	r += 104 * n * math.floor(math.log(n))
	r += 120 * n
	r -= 52 * math.floor(math.log(n))
	r -= 74
	print(int(r))