from hybrid import Hybrid
from point import Point
from bitstring import *
import secrets
import json

def printList(bytedata):
    bits = Bits(bytes = bytedata).bin
    lst = []
    for i in bits: 
        lst.append(int(i))
    return lst

rounds = 6

l = secrets.token_bytes(16)
address = secrets.token_bytes(32)
print('l: \n  {}\n'.format(printList(l)))
print('address: \n  {}\n'.format(printList(address)))

h_reg = Hybrid()
pk_reg, sk_reg = h_reg.getKeys()
print('pk_reg: \n  {}\n  {}\n'.format(pk_reg.x, pk_reg.y))
print('sk_reg: \n  {}\n'.format(printList(sk_reg)))

l_ctxt, l_tag, l_c1, l_c2, l_r = h_reg.encrypt(l)
print('rand_reg: \n  {}\n'.format(l_r))

m = l_ctxt + address
print('l_ctxt: \n  {}\n'.format(l_ctxt))
print('l_tag: \n  {}\n'.format(l_tag))
print('address: \n  {}\n'.format(address))
print('m: \n  {}\n'.format(m))

h_enc = []
for i in range(0, rounds):
    h_enc.append(Hybrid())

ptxt = [None] * (rounds + 1)
ptxt[0] = m
tag = [None] * rounds
c1 = [None] * rounds
c2 = [None] * rounds
r = [None] * rounds
pk_list = [None] * rounds
sk_list = [None] * rounds

for i in range(0, rounds):
    pk, sk = h_enc[i].getKeys()
    pk_list[i] = [str(pk.x), str(pk.y)]
    sk_list[i] = printList(sk)
    print('Encryption node ({})'.format(i))
    print('pk: \n  {}\n  {}\n'.format(pk.x, pk.y))
    print('sk: \n  {}\n'.format(printList(sk)))

for i in range(0, rounds):
    ptxt[i+1], tag[i], c1[i], c2[i], r[i] = h_enc[i].encrypt(ptxt[i])
    print('Encryption process ({})'.format(i))
    print('r: \n  {}\n'.format(r[i]))
    print('C1: \n  {}\n'.format(c1[i]))
    print('c2: \n  {}\n'.format(printList(c2[i].bytes)))
    print('ctxt: \n  {}\n'.format(printList(ptxt[i+1])))
    print('auth_tag: \n  {}\n'.format(printList(tag[i])))

ctxt = ptxt[rounds]
print('ctxt: \n  {}\n'.format(printList(ctxt)))

# Pre-json format to Circom
r_str = []
c1_str = []
c2_lst = []
for i in range(0, rounds):
    r_str.append(str(r[i]))
    c1_str.append([str(c1[i].x), str(c1[i].y)])
    c2_lst.append(printList(c2[i].bytes))

input_data = {
    "l": printList(l),
    "k_reg": printList(sk_reg),
    "pk_reg": [
        str(pk_reg.x),
        str(pk_reg.y)
    ],
    "rand_reg": str(l_r),
    "l_ctxt": printList(l_ctxt),
    "l_tag": printList(l_tag),
    "l_c1": [
        str(l_c1.x),
        str(l_c1.y)
    ],
    "l_c2": printList(l_c2.bytes),
    "address": printList(address),
    "k": sk_list,
    "pk": pk_list,
    "rand": r_str,
    "inpt_ctxt": printList(ctxt),
    "inpt_eg_c1": c1_str,
    "inpt_eg_c2": c2_lst
}
json_data = json.dumps(input_data)
print('JSON data: \n{}'.format(json_data))