from hashlib import sha256

# input message m
m = 2
print("m")
print(m.to_bytes(32, 'little'))

# input key preC2
preC2_x = 7343892471798980115039601227761641590656022205835054301413211368611917152065
preC2_y = 6258896638184247396732122212047772494546646465258962849180339877692621123077
print("preC2")
print(preC2_x.to_bytes(32, 'little'))
print(preC2_y.to_bytes(32, 'little'))

# compute hash(preC2)
h = sha256()
h.update(preC2_x.to_bytes(32, 'little'))
h.update(preC2_y.to_bytes(32, 'little'))
res = h.digest()
print("hash(preC2)")
print(res)

def byte_xor(ba1, ba2):
	return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])
	
def num2bits(a, n):
	out = [0] * n
	lc1 = 0
	e2 = 1
	for i in range(0, n):
		out[i] = (a >> i) & 1
		lc1 += out[i] * e2
		e2 = e2 + e2
	return out
	
def bits2num(a, n):
	lc1 = 0
	e2 = 1
	for i in range(0, n):
		lc1 += a[i] * e2
		e2 = e2 + e2
	return lc1

xor = byte_xor(m.to_bytes(32, 'little'), res)
print("XOR")
print(xor)

def access_bit(data, num):
	base = int(num // 8)
	shift = int(num % 8)
	return (data[base] >> shift) & 0x1
	
xor_bits = [access_bit(xor, i) for i in range(len(xor)*8)]
print(xor_bits)

print("c2 as number")
print(bits2num(xor_bits, 256))

