from sage.all_cmdline import *
from point import Point
from babyjubjub import BabyJubJub
import secrets
from hashlib import sha256
from utils import bytearray_to_bitlist, num2bits, bitstring_to_bytes
from binascii import hexlify, unhexlify
from bitstring import *

# ElGamal #	
class ElGamal:
	
	# Interfaces edwards points by default (else montgomery)
	def __init__(self, privKey, edwards = True):
		self._weierCurve = BabyJubJub()
		self._privKey = Integer(privKey)
		montB = self._weierCurve.getBaseCoordMont()
		self._montB = self._weierCurve.getCurvePoint(montB)
		self._pubKey = self._privKey * self._montB
		self._edwards = edwards
		
	def getPrivateKey(self):
		return self._privKey
	
	def getPublicKey(self):
		if(self._edwards):
			return self._weierCurve.MontToEdw(Point(self._pubKey[0], self._pubKey[1]))
		else:
			return Point(self._pubKey[0], self._pubKey[1])
		
	def encrypt(self, M):
		if(self._edwards):
			Mmont = self._weierCurve.EdwToMontCurvePoint(M)
		else:
			Mmont = self._weierCurve.getCurvePoint(M)
			
		r = secrets.randbits(256)
		C1 = r * self._montB
		preC2 = r * self._pubKey
		C2 = preC2 + Mmont
		
		if(self._edwards):
			C1p = self._weierCurve.MontToEdw(Point(C1[0], C1[1]))
			C2p = self._weierCurve.MontToEdw(Point(C2[0], C2[1]))
		else:
			C1p = Point(C1[0], C1[1])
			C2p = Point(C2[0], C2[1])
		
		return C1p, C2p
		
	def decrypt(self, C1p, C2p):
		if(self._edwards):
			C1 = self._weierCurve.EdwToMontCurvePoint(C1p)
			C2 = self._weierCurve.EdwToMontCurvePoint(C2p)
		else:
			C1 = self._weierCurve.getCurvePoint(C1p)
			C2 = self._weierCurve.getCurvePoint(C2p)
	
		S = self._privKey * C1
		M = C2 - S
		if(self._edwards):
			Mp = self._weierCurve.MontToEdw(Point(M[0], M[1]))
		else:
			Mp = Point(M[0], M[1])
		
		return Mp

# ElGamalHashed #
# TODO: Accept more than integers: to_bytes() only works for int
class ElGamalHashed:
	
	# Interfaces edwards points with class Point
	def __init__(self, pubKey = None):
		if pubKey == None:		# Init to decrypt
			self._weierCurve = BabyJubJub()
			self._privKey = Integer(secrets.randbits(256))
			self._edwB = self._weierCurve.getBaseCoordEdw()
			self._pubKey = self._weierCurve.scalarMul(self._privKey, self._edwB)
		else:					# Init to encrypt
			self._weierCurve = BabyJubJub()
			self._privKey = None
			self._pubKey = pubKey
			self._edwB = self._weierCurve.getBaseCoordEdw()
		
	def getPrivateKey(self):
		return self._privKey
	
	def getPublicKey(self):
		return self._pubKey

	'''
		Input format: bytes, int
	'''	
	def encrypt(self, M):
	
		plaintext = None
		if type(M) is bytes:
			plaintext = Bits(bytes=M)
		elif type(M) is int:
			plaintext = M.to_bytes(32, 'little')
		else:
			print('Error in plaintext type')
		
		r = int(secrets.randbits(100))
		C1 = self._weierCurve.scalarMul(r, self._edwB)
		preC2 = self._weierCurve.scalarMul(r, self._pubKey)
		
		preC2_x_bits = num2bits(int(preC2.x), 256)
		preC2_y_bits = num2bits(int(preC2.y), 256)
		preC2_str = "0b"
		for e in preC2_x_bits:
			preC2_str += str(e)
		for e in preC2_y_bits:
			preC2_str += str(e)
		preC2_hex = Bits(preC2_str).hex
		preC2_bytes = unhexlify(preC2_hex)

		h = sha256()
		#h.update(int(preC2.x).to_bytes(32, 'big'))
		#h.update(int(preC2.y).to_bytes(32, 'big'))
		h.update(preC2_bytes)
		res = h.digest()
		bin_res = Bits(bytes=res)
		c2 = plaintext ^ bin_res
		
		return C1, c2, r
	
	def decrypt(self, C1, c2):
		if(self._privKey == None):
			return None
		else:
			S = self._weierCurve.scalarMul(self._privKey, C1)
			h = sha256()
			h.update(int(S.x).to_bytes(32, 'little'))
			h.update(int(S.y).to_bytes(32, 'little'))
			res = h.digest()
			M = self._byte_xor(c2, res)
			
			return M
		
	def _byte_xor(self, ba1, ba2):
		return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])
