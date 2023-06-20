# Performs elgamal encryption and decryption
# Interface curve is in Edwards form
# Montgomery is needed for internal working

def EdwToMont(x,y):
	u = (Fq(1)+Fq(y))/(Fq(1)-Fq(y))
	v = (Fq(1)+Fq(y))/((Fq(1)-Fq(y))*Fq(x))
	return u,v
	
def MontToEdw(u,v):
	x = Fq(u)/Fq(v)
	y = (Fq(u)-Fq(1))/(Fq(u)+Fq(1))
	return x,y
	
# Curve generation	
q = 21888242871839275222246405745257275088548364400416034343698204186575808495617

Fq.<x,y> = GF(21888242871839275222246405745257275088548364400416034343698204186575808495617)[]

MontCurve = EllipticCurve(y^2-(x^3+168698*x^2+x))

print(MontCurve)

Bedw_x = 5299619240641551281634865583518297030282874472190772894086521144482721001553
Bedw_y = 16950150798460657717958625567821834550301663161624707787222815936182638968203

Bmont_x, Bmont_y = EdwToMont(Bedw_x, Bedw_y)
Bmont = MontCurve(Bmont_x, Bmont_y)

# Key generation
sk = 3
pk = 3 * Bmont
#print("secret key")
#print(sk)
#print("public key")
#print(pk)

# Message generation
Medw_x = 17777552123799933955779906779655732241715742912184938656739573121738514868268
Medw_y = 2626589144620713026669568689430873010625803728049924121243784502389097019475

Mmont_x, Mmont_y = EdwToMont(Medw_x,Medw_y)
Mmont = MontCurve(Mmont_x, Mmont_y)
print("Mmont:")
print(Mmont)

# Encryption
k = 12345
C1 = k * Bmont
preC2 = (k * pk)
C2 = preC2 + Mmont
#print("C1: ")
#print(C1)
#print("C2: ")
#print(C2)

# Decryption
S = sk * C1
MM = C2 - S
print("MM: ")
print(MM)

#####################
print("Edwards message: ")
print(Medw_x)
print(Medw_y)

PKedw_x, PKedw_y = MontToEdw(pk[0], pk[1])
print("Edwards public key: ")
print(PKedw_x)
print(PKedw_y)

print("Secret key: ")
print(sk)

print("Randomness: ")
print(k)

C1edw_x, C1edw_y = MontToEdw(C1[0], C1[1])
print("Edwards ciphertext 1: ")
print(C1edw_x)
print(C1edw_y)
C2edw_x, C2edw_y = MontToEdw(C2[0], C2[1])
print("Edwards ciphertext 2: ")
print(C2edw_x)
print(C2edw_y)
preC2edw_x, preC2edw_y = MontToEdw(preC2[0], preC2[1])
print("Edwards preC2: ")
print(preC2edw_x)
print(preC2edw_y)
