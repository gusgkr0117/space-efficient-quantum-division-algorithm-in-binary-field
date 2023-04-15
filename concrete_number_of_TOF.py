import math


items = [8, 16, 127, 163, 233, 283, 571]
modmul_tof = [27, 81, 2185, 4387, 6323, 10273 ,31171]

# TOF_new : 13*n^2 + 40*n*logn + n - 20*logn - 8
TOF_new = []
for n in items:
	r = 13 * n ** 2
	r += 40 * n * math.floor(math.log(n,2))
	r += n
	r -= 20 * math.floor(math.log(n,2))
	r -= 8
	TOF_new.append(r)

# TOF_org : 12*n^2 + 88*n*logn + 116*n - 44*logn -62
TOF_org = []
for n in items:
	r = 12 * n ** 2
	r += 88 * n * math.floor(math.log(n,2))
	r += 116 * n
	r -= 44 * math.floor(math.log(n,2))
	r -= 62
	TOF_org.append(r)

# qubits_new : 6*n + 4 * logn + 10
qubit_new = []
for n in items:
	r = 6 * n
	r += 4 * math.floor(math.log(n,2))
	r += 10
	qubit_new.append(r)

# qubits_org : 7*n + logn + 8
qubit_org = []
for n in items:
	r = 7 * n
	r += math.floor(math.log(n,2))
	r += 8
	qubit_org.append(r)

for i in range(len(items)):
	TOF_new[i] += modmul_tof[i]
	TOF_org[i] += modmul_tof[i]
	print(str(items[i]) + "\t&" + str(qubit_org[i]) + "\t&" + str(TOF_org[i]) + "\t&" + str(qubit_new[i]) + "\t&" + str(TOF_new[i]) + "\t&%.3f" % ((qubit_new[i] - 3*items[i])/(qubit_org[i] - 3*items[i])) + "\t&%.3f" % (TOF_new[i]/TOF_org[i]) + "\\\\")