from point import *
from sage.all_cmdline import *

Fq = GF(21888242871839275222246405745257275088548364400416034343698204186575808495617)

a = 168700
d = 168696

def checkPoint(P):
    left = Fq(a) * Fq(P.x) * Fq(P.x) + Fq(P.y) * Fq(P.y)
    right = Fq(1) + Fq(d) * Fq(P.x) * Fq(P.x) * Fq(P.y) * Fq(P.y)
    return left == right

def add(P1, P2):
    if checkPoint(P1) and checkPoint(P2):
        x_top = Fq(P1.x) * Fq(P2.y) + Fq(P1.y) * Fq(P2.x)
        x_bot = Fq(1) + Fq(d) * Fq(P1.x) * Fq(P2.x) * Fq(P1.y) * Fq(P2.y)
        y_top = Fq(P1.y) * Fq(P2.y) - Fq(a) * Fq(P1.x) * Fq(P2.x)
        y_bot = Fq(1) - Fq(d) * Fq(P1.x) * Fq(P2.x) * Fq(P1.y) * Fq(P2.y)
        return Point(x_top / x_bot, y_top / y_bot)
    else:
        return Point(0, 0)

def add_t(P1, P2):
    x_top = P1.x * P2.y + P1.y * P2.x
    x_bot = 1 + d * P1.x * P2.x * P1.y * P2.y
    y_top = P1.y * P2.y - a * P1.x * P2.x
    y_bot = 1 - d * P1.x * P2.x * P1.y * P2.y
    return Point(x_top / x_bot, y_top / y_bot)

def testx(P1, P2):
    return Fq(P1.x) * Fq(P2.x)

def testy(P1, P2):
    return Fq(P1.y) * Fq(P2.y)