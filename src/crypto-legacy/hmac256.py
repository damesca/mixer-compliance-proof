from hashlib import sha256
from bitstring import *

class hmac256:

    def __init__(self):
        self._opad = BitArray('0x5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c')
        self._ipad = BitArray('0x36363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636')

    def digest(self, key, message):
        okeypad = self._opad
        ikeypad = self._ipad
        okeypad[0:256] = key ^ okeypad[0:256]
        ikeypad[0:256] = key ^ ikeypad[0:256]

        h1 = sha256()
        h1.update(ikeypad.bytes)
        h1.update(message)
        hashsum1 = h1.digest()

        h2 = sha256()
        h2.update(okeypad.bytes)
        h2.update(hashsum1)
        hashsum2 = h2.digest()

        return hashsum2


def printList(bytedata):
    bits = Bits(bytes = bytedata).bin
    lst = []
    for i in bits: 
        lst.append(int(i))
    return lst

h = hmac256()
key = BitArray('0x0101010101010101010101010101010101010101010101010101010101010101')
message = BitArray('0x01')
res = h.digest(key.bytes, message.bytes)
print(printList(key.bytes))
print(printList(message.bytes))
print(BitArray(bytes = res).bin)