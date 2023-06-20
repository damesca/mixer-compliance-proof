def num2bits(inp, n):
	out = [0] * n
	lc1 = 0
	e2 = 1
	for i in range(0, n):
		out[i] = (inp >> i) & 1
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
	
def access_bit(data, num):
	base = int(num // 8)
	shift = int(num % 8)
	return (data[base] >> shift) & 0x1
	
def bytearray_to_bitlist(data):
	return [access_bit(data, i) for i in range(len(data)*8)]
	
def xor_bytearrays(ba1, ba2):
	return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def concat(e, a=None):
    res = ""
    for i in e:
        res = res + str(i)
    if a != None:
        for j in a:
            res = res + str(j)
    return res

def bitstring_to_bytes(s, little=True):
    if little:
        return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='little')
    else:
        return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')