from babyjubjub import *
from point import Point
from sage.all_cmdline import *
from utils import num2bits
from math import log2, floor
from twistedEdwards import checkPoint, add, testx, testy, add_t

BASE_EDW = Point(5299619240641551281634865583518297030282874472190772894086521144482721001553, 16950150798460657717958625567821834550301663161624707787222815936182638968203)

Fp = GF(21888242871839275222246405745257275088548364400416034343698204186575808495617)
curve = BabyJubJub()

def doubleAndAdd(curve, exp, P):
    n = floor(log2(exp))
    bits = num2bits(exp, n+1)
    i = len(bits) - 2
    res = P
    while i >= 0:
        res = add(res, res)
        if bits[i] == 1:
            res = add(res, P)
        i = i - 1
    return res

def testEscalarMul(curve, BASE_EDW, r):
    #BASE_MONT = curve.EdwToMont(BASE_EDW)
    #BASE_WEIER = curve.MontToWeier(BASE_MONT)
    #BASE_WEIER_cp = curve.getCurvePoint(BASE_WEIER)
    print(checkPoint(BASE_EDW))

    RES = doubleAndAdd(curve, r, BASE_EDW)
    print(checkPoint(RES))

    #test_WEIEREXP = Point(test_WEIEREXP_cp[0], test_WEIEREXP_cp[1])
    #test_MONTEXP = curve.WeierToMont(test_WEIEREXP)
    #test_EDWEXP = curve.MontToEdw(test_MONTEXP)
    print('<<EscalarMul>>\n- r: {} -\n- RES.x: {}\n- RES.y: {}\n\n'.format(
        r, RES.x, RES.y
    ))

def testAddIterative(curve, BASE_EDW, r):
    P1 = curve.getCurvePoint(
        curve.MontToWeier(curve.EdwToMont(BASE_EDW))
    )
    for i in range(1, r):
        P1 += P1
    Res = curve.MontToEdw(curve.WeierToMont(Point(P1[0], P1[1])))
    print('<<AddIterative>>\n- r: {} -\n- RES.x: {}\n- RES.y: {}\n\n'.format(
        r, Res.x, Res.y
    ))
'''
escalar = [2, 20, 200, 2000, 20000, 200000]
for e in escalar:
    testEscalarMul(curve, BASE_EDW, e)
    testAddIterative(curve, BASE_EDW, e)
'''
x1 = 17777552123799933955779906779655732241715742912184938656739573121738514868268
y1 = 2626589144620713026669568689430873010625803728049924121243784502389097019475

x2 = 16540640123574156134436876038791482806971768689494387082833631921987005038935
y2 = 20819045374670962167435360035096875258406992893633759881276124905556507972311

P1 = Point(x1, y1)
P2 = Point(x2, y2)

print(add(P1, P2))
print(add_t(P1, P2))
print("")
print(add(P1, P1))
print(add_t(P1, P1))
print(testx(P1, P2))
print(testy(P1, P2))