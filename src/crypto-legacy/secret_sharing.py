from sage.all_cmdline import *
from secrets import randbelow

# Additive Secret Sharing #
class SecretSharing:

	def __init__(self):
		self._q = Integer(21888242871839275222246405745257275088548364400416034343698204186575808495617)
		self._Fq = GF(self._q)
		
	def share(self, s, n):
		if type(s) is bytes:
			s = int.from_bytes(s, 'big')

		shares = []
		for i in range(0, n-1):
			shares.append(self._Fq(randbelow(21888242871839275222246405745257275088548364400416034343698204186575808495617)))
		last = self._Fq(s)
		for i in range(0, n-1):
			last = last - shares[i]
		shares.append(last)
		return shares
		
	def recombine(self, shares):
		res = self._Fq(0)
		for i in shares: res = res + i
		return res
		
