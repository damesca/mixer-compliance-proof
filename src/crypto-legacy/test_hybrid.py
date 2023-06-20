from elgamal import ElGamal, ElGamalHashed
from utils import bitstring_to_bytes, bytearray_to_bitlist
from point import Point
from bitstring import *
from Crypto.Cipher import AES

# Message #
msg_big = '10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
msg = Bits(bin = msg_big)
print('Message: \n  {}'.format(msg.bytes))

# AES encryption #
k_big = '1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
k = Bits(bin = k_big)
print('Secret key: \n  {}'.format(k.bytes))

nonce_big = '1000000000000000000000000000000000000000000000000000000000000000'
nonce = Bits(bin = nonce_big)
print('AES nonce: \n  {}'.format(nonce.bytes))

cipher = AES.new(k.bytes, AES.MODE_CTR, nonce = nonce.bytes)
ciphertext = cipher.encrypt(msg.bytes)
print('AES ciphertext: \n  {}'.format(Bits(bytes = ciphertext).bin))

# ElGamal encryption #
eg = ElGamalHashed()
regPK = eg.getPublicKey()
print('Public key.x: \n  {}'.format(regPK.x))
print('Public key.y: \n  {}'.format(regPK.y))

c1, c2, r = eg.encrypt(k.bytes)
print('Randomness: \n  {}'.format(r))
print('ElGamal c1.x: \n  {}'.format(c1.x))
print('ElGamal c1.y: \n  {}'.format(c1.y))
c2_list = bytearray_to_bitlist(c2)
c2_str = ''
for e in c2_list:
    c2_str += str(e)
print('ElGamal c2: \n  {}'.format(c2.bin))