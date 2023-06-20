from sage.all_cmdline import *
from point import Point

# Constants #
PRIME = 21888242871839275222246405745257275088548364400416034343698204186575808495617
A_MONT = 168698
B_MONT = 1
A_WEIER = 7296080957279758407415468581752425029516121466805344781232734728849116493472
B_WEIER = 16213513238399463127589930181672055621146936592900766180517188641980520820846

# BabyJubJub #
class BabyJubJub:

	def __init__(self):
		self._q = Integer(21888242871839275222246405745257275088548364400416034343698204186575808495617)
		#self._Fq = GF(self._q)['x, y']
		self._Fq = GF(self._q)
		#(self._x, self._y) = self._Fq._first_ngens(2)
		#self._MontCurve = EllipticCurve(self._y**Integer(2) -(self._x**Integer(3) +Integer(168698) *self._x**Integer(2) +self._x))
		self._Bedw = Point(Integer(5299619240641551281634865583518297030282874472190772894086521144482721001553), Integer(16950150798460657717958625567821834550301663161624707787222815936182638968203))
		self._Bmont = self.EdwToMont(self._Bedw)
		self._AMont = 168698
		self._BMont = 1
		self._aWeir = 7296080957279758407415468581752425029516121466805344781232734728849116493472
		self._bWeir = 16213513238399463127589930181672055621146936592900766180517188641980520820846
		self._WeirCurve = EllipticCurve(self._Fq, [self._aWeir, self._bWeir])
		self.P = Point(17777552123799933955779906779655732241715742912184938656739573121738514868268, 2626589144620713026669568689430873010625803728049924121243784502389097019475)

	def EdwToMont(self, pe):
		x = (self._Fq(Integer(1))+self._Fq(pe.y))/(self._Fq(Integer(1))-self._Fq(pe.y))
		y = (self._Fq(Integer(1))+self._Fq(pe.y))/((self._Fq(Integer(1))-self._Fq(pe.y))*self._Fq(pe.x))
		return Point(x, y)
		
	def MontToEdw(self, pm):
		x = self._Fq(pm.x)/self._Fq(pm.y)
		y = (self._Fq(pm.x)-self._Fq(Integer(1)))/(self._Fq(pm.x)+self._Fq(Integer(1)))
		return Point(x,y)
		
	def EdwToMontCurvePoint(self, pe):
		pm = self.EdwToMont(pe)
		return self.getCurvePoint(pm)

	def printCurve(self):
		print(self._WeirCurve)
		
	def getBaseCoordEdw(self):
		return self._Bedw
		
	def getBaseCoordMont(self):
		return self._Bmont
		
	def getCurvePoint(self, p):
		return self._WeirCurve(p.x, p.y)

	def MontToWeier(self, p):
		x = self._Fq(p.x) / self._Fq(B_MONT) + self._Fq(A_MONT) / (self._Fq(3) * self._Fq(B_MONT))
		y = self._Fq(p.y) / self._Fq(B_MONT)
		return Point(x, y)

	def WeierToMont(self, p):
		x = self._Fq(B_MONT) * (self._Fq(p.x) - self._Fq(A_MONT) / (self._Fq(3) * self._Fq(B_MONT)))
		y = self._Fq(B_MONT) * self._Fq(p.y)
		return Point(x, y)

	def add(self, p1, p2):
		weierP1 = self.MontToWeier(self.EdwToMont(p1))
		weierP2 = self.MontToWeier(self.EdwToMont(p2))
		weierP1c = self.getCurvePoint(weierP1)
		weierP2c = self.getCurvePoint(weierP2)
		P3c = weierP1c + weierP2c
		weierP3 = Point(P3c[0], P3c[1])
		return self.MontToEdw(self.WeierToMont(weierP3))

	def scalarMul(self, e, P):
		weierP = self.MontToWeier(self.EdwToMont(P))
		weierPc = self.getCurvePoint(weierP)
		ePc = Integer(e) * weierPc
		eP = Point(ePc[0], ePc[1])
		return self.MontToEdw(self.WeierToMont(eP))