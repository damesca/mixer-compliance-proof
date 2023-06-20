from babyjubjub import BabyJubJub
from point import Point
from secrets import randbits

class Pedersen:

    def __init__(self):
        self._base = Point(5299619240641551281634865583518297030282874472190772894086521144482721001553, 16950150798460657717958625567821834550301663161624707787222815936182638968203)
        self._curve = BabyJubJub()

    def commit(self, x, r):
        if type(x) is bytes:
            x = int.from_bytes(x, 'big')
        if type(r) is bytes:
            r = int.from_bytes(r, 'big')

        #r = randbits(256)
        p1 = self._curve.scalarMul(x, self._base)
        p2 = self._curve.scalarMul(r, self._base)
        comm = self._curve.add(p1, p2)
        
        return comm

    def add(self, comm1, comm2):
        return self._curve.add(comm1, comm2)
