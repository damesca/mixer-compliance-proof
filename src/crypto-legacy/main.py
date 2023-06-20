from elgamal import ElGamal, ElGamalHashed
from point import Point
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from sage.all_cmdline import *
from hybrid import Hybrid
import secrets
from binascii import hexlify

if __name__ == '__main__':
	
	# Generate Regulator
	print("\n#--- Generating regulator keys ---#\n")
	regHenc = ElGamalHashed()
	regPK = regHenc.getPublicKey()
	
	print('Regulator public key: {}'.format(regPK))
	
	# Generate Alice params
	print("\n#--- Generating Alice params ---#\n")
	address = secrets.randbits(160).to_bytes(20, 'little')
	l1 = secrets.randbits(256)#.to_bytes(32, 'little')
	aliceHenc = ElGamalHashed(regPK)
	l2_C1p, l2_c2 = aliceHenc.encrypt(l1)
	
	l2_C1p_x = int(l2_C1p.x).to_bytes(32, 'little')
	l2_C1p_y = int(l2_C1p.y).to_bytes(32, 'little')
	
	m = address + l2_C1p_x + l2_C1p_y + l2_c2
	
	print('address: {}'.format(hexlify(address)))
	print('l1: {}'.format(hexlify(l1.to_bytes(32, 'little'))))
	print('l2_C1p: {}'.format(l2_C1p))
	print('l2_c2: {}'.format(hexlify(l2_c2)))
	print('m: {}'.format(hexlify(m)))
	
	# Generate mixnet keys
	print("\n#--- Generating mixnet keys ---#\n")
	n = 5
	mixnet = []
	mixnetPK = []
	for i in range(0, n):
		mixnetHenc = Hybrid()
		mixnet.append(mixnetHenc)
		mixnetPK.append(mixnetHenc.getPublicKey())
		print('Mixnet({}) PK: {}'.format(i, mixnetPK[i]))
		
	# Generate alice encryptors
	print("\n#--- Alice receives mixnet PKs ---#\n")
	aliceMenc = []
	for i in range(0, n):
		aliceMenc.append(Hybrid(mixnetPK[i]))
	
	# Sequential encryption
	print("\n#--- Generating sequential encryption ---#\n")
	encryptedKeys = []
	ciphertexts = [m]
	
	for i in range(0, n):
		c, c_t, c_n, c_C1p, c_c2 = aliceMenc[i].encrypt(ciphertexts[i])
		ctx = c_n + c_t + c
		ciphertexts.append(ctx)
		encryptedKeys.append((c_C1p, c_c2))
		
		print('({}) c: {}'.format(i, hexlify(c)))
		print('({}) c_t: {}'.format(i, hexlify(c_t)))
		print('({}) c_n: {}\n'.format(i, hexlify(c_n)))
		
	print("\n#--- A -> M[n]: ctxn, [EncK0, EncK1, ..., EncKn] ---#\n")
	
	# Sequential decryption
	print("\n#--- Generating sequential decryption ---#\n")
	decryptions = []

	for i in range(n, 0, -1):
		c_n = ciphertexts[i][:16]
		c_t = ciphertexts[i][16:32]
		c = ciphertexts[i][32:len(ciphertexts[i])]
		c_encKey = encryptedKeys[i-1]
		data = mixnet[i-1].decrypt(c, c_t, c_n, c_encKey[0], c_encKey[1])
		decryptions.append(data)
		
	new_m = decryptions[n-1]
	print('Original m: {}'.format(hexlify(new_m)))
	
	# Regulator decrypts message
	print("\n#--- Regulator decrypts message ---#\n")
	
	a = 0
	b = 20
	reg_addr = new_m[a:b]
	a = b
	b += 32
	reg_l2C1x = int.from_bytes(new_m[a:b], 'little')
	a = b
	b += 32
	reg_l2C1y = int.from_bytes(new_m[a:b], 'little')
	a = b
	reg_l2c2 = new_m[a:]
	
	reg_l2C1 = Point(reg_l2C1x, reg_l2C1y)
	
	val = regHenc.decrypt(reg_l2C1, reg_l2c2)
	
	print('address: {}'.format(hexlify(reg_addr)))
	print('l2_C1p: {}'.format(reg_l2C1))
	print('l2_c2: {}'.format(hexlify(reg_l2c2)))
	print('l1: {}'.format(hexlify(val)))
	
	'''
	# ElGamal
	Medw_x = Integer(17777552123799933955779906779655732241715742912184938656739573121738514868268) 
	Medw_y = Integer(2626589144620713026669568689430873010625803728049924121243784502389097019475) 
	M = Point(Medw_x, Medw_y)
	print('> M: {}'.format(M))

	elgamal = ElGamal(3)
	print('> privKey: {}'.format(elgamal.getPrivateKey()))
	print('> pubKey: {}'.format(elgamal.getPublicKey()))
	C1, C2 = elgamal.encrypt(M)
	print('> C1: {}'.format(C1))
	print('> C2: {}'.format(C2))
	D = elgamal.decrypt(C1, C2)
	print('> D: {}'.format(D))
	
	# AES
	data = b'secret data'
	key = get_random_bytes(16)
	cipher = AES.new(key, AES.MODE_EAX)
	nonce = cipher.nonce
	ciphertext, tag = cipher.encrypt_and_digest(data)
	print('> ciphertext: {}'.format(ciphertext))
	decipher = AES.new(key, AES.MODE_EAX, nonce)
	data = decipher.decrypt_and_verify(ciphertext, tag)
	print('> data: {}'.format(data))
	
	# ElGamalHashed
	m = 55
	print('> m: {}'.format(m.to_bytes(32, 'little')))
	elgamalh = ElGamalHashed(3)
	CH1, ch2 = elgamalh.encrypt(m)
	print('> CH1: {}'.format(CH1))
	print('> ch2: {}'.format(ch2))
	d = elgamalh.decrypt(CH1, ch2)
	print('> d: {}'.format(d))
	
	# Hybrid
	
	aHybrid = Hybrid()
	pubKey = aHybrid.getPublicKey()
	print('> Alice public key: {}'.format(pubKey))
	
	bHybrid = Hybrid(pubKey)
	message = b'message'
	c, t, n, C1p, c2 = bHybrid.encrypt(message)
	print('> Encrypted message: {}'.format(c))
	print('> Encrypted key: [{},{}]'.format(C1p, c2))
	
	data = aHybrid.decrypt(c, t, n, C1p, c2)
	print('> Decrypted data: {}'.format(data))
	'''
	
