from elgamal import ElGamalHashed
from point import Point
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from sage.all_cmdline import *
import secrets
from bitstring import *
from hashlib import sha256
from hmac256 import hmac256

# Hybrid encryption for one message

class Hybrid:

	def __init__(self, pubKey = None):
		if pubKey == None:		# Init to decrypt
			self._elgamal = ElGamalHashed()
			self._privKey = self._elgamal.getPrivateKey()
			self._pubKey = self._elgamal.getPublicKey()
			self._symmKey = secrets.token_bytes(32)
		else:					# Init to encrypt
			self._elgamal = ElGamalHashed(pubKey)
			self._privKey = None
			self._pubKey = pubKey
			self._symmKey = secrets.token_bytes(32)
	
	def getKeys(self):
		return self._pubKey, self._symmKey
		
	#def getPublicKey(self):
	#	return self._pubKey
		
	#def _encryptKey(self):
	#	self._C1p, self._c2 = self._elgamal.encrypt(int(self._symmKey))
		
	def encrypt(self, msg):
		
		#nonce_big = '1000000000000000000000000000000000000000000000000000000000000000'
		#nonce_bytes = Bits(bin = nonce_big).bytes
		cipher = AES.new(self._symmKey, AES.MODE_ECB)
		ciphertext = cipher.encrypt(msg)

		hmac = hmac256()
		tag = hmac.digest(self._symmKey, msg)
		
		c1, c2, r = self._elgamal.encrypt(self._symmKey)
		return ciphertext, tag, c1, c2, r

	# TODO	
	def decrypt(self):
		return None