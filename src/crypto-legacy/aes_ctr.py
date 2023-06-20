from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from utils import bytearray_to_bitlist
import secrets
import json
from bitstring import *

def printList(bytedata):
    bits = Bits(bytes = bytedata).bin
    lst = []
    for i in bits: 
        lst.append(int(i))
    return lst

#key = secrets.token_bytes(32)
#msg = secrets.token_bytes(32)

msg = Bits(hex = '7c6caf568eebf5b54d4b1a5902a07ae5b0ed6b7703da32e580112dc813ee47fb')
key = Bits(hex = 'b173d9ca358a2a4519c265a9567eadb841c19b29c6ce959aa4c68a1ae0bc68ea')

nonce_big = '0000000000000000000000000000000000000000000000000000000000000000'
nonce_bytes = Bits(bin = nonce_big).bytes
cipher = AES.new(key.bytes, AES.MODE_CTR, nonce = nonce_bytes, initial_value = 0)
#cipher = AES.new(key, AES.MODE_CTR)
#nonce_alt = cipher.nonce
ciphertext = cipher.encrypt(msg.bytes)

print('Message: \n  {}\n'.format(msg))
print('Key: \n  {}\n'.format(key))
#print('Nonce: \n  {}\n'.format(Bits(bytes = nonce_alt).hex))
print('Nonce: \n  {}\n'.format(nonce_bytes))
print('Ciphertext: \n  {}\n'.format(printList(ciphertext)))

input_data = {
    "MSG": printList(msg.bytes),
    "CTR": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "KEY": printList(key.bytes)
}

json_data = json.dumps(input_data)
print('JSON data: \n{}'.format(json_data))