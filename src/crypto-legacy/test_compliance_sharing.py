from pedersen import Pedersen
from secret_sharing import SecretSharing
from secrets import token_bytes
from hybrid import Hybrid
from point import Point
from bitstring import *
from Crypto.Util.Padding import pad
import json

def printList(bytedata):
    bits = Bits(bytes = bytedata).bin
    lst = []
    for i in bits: 
        lst.append(int(i))
    return lst

n = 4

l = token_bytes(11)     #88 bits
addr = token_bytes(20)  # 160 bits

# 88 + 160 = 248 < 253 (nº bits of p)

print('l: \n  {}\n'.format(l))
print('addr: \n  {}\n'.format(addr))

enc = Hybrid()
l_ctxt, l_tag, l_C1, l_c2, r = enc.encrypt(pad(l, 16))

print('l_ctxt: \n  {}\n'.format(l_ctxt))
print('l_C1: \n  {}\n'.format(l_C1))
print('l_c2: \n  {}\n'.format(l_c2))
print('r: \n  {}\n'.format(r))

x = l + addr
cr = token_bytes(30)
print('x: \n  {}\n'.format(int.from_bytes(x, 'big')))
print('cr: \n  {}\n'.format(int.from_bytes(cr, 'big')))

ss = SecretSharing()
x_sh = ss.share(x, n)
cr_sh = ss.share(cr, n)
print('x_sh: \n  {}\n'.format(x_sh))
print('cr_sh: \n  {}\n'.format(cr_sh))

print('x-rec: \n  {}\n'.format(ss.recombine(x_sh)))
print('cr-rec: \n  {}\n'.format(ss.recombine(cr_sh)))

pd = Pedersen()
mac = pd.commit(x, r)
print('mac: \n  {}\n'.format(mac))

x_shares_list = [None] * n
r_shares_list = [None] * n
for i in range(0, n):
    x_shares_list[i] = str(x_sh[i])
    r_shares_list[i] = str(cr_sh[i])

pk_reg, sk_reg = enc.getKeys()

l_list = printList(l)
while len(l_list) < 128:
    l_list.append(0)

input_data = {
    "x": str(int.from_bytes(x, 'big')),
    "r": str(r),
    "x_shares": x_shares_list,
    "r_shares": r_shares_list,
    "mac": [
        str(mac.x),
        str(mac.y)
    ],
    "m": l_list,
    "k": printList(sk_reg),
    "pk": [
        str(pk_reg.x),
        str(pk_reg.y)
    ],
    "rand": str(r)
}

#print(input_data)
json_data = json.dumps(input_data)
print('JSON data: \n{}'.format(json_data))