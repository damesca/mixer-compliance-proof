pragma circom 2.0.0;

include "escalarmulany.circom";
include "bitify.circom";
include "babyjub.circom";

/*
 * Encrypts an ElGamal ciphertext with BabyJubJub EC in twisted edw form
 *
 * public input Y: public key point
 * public input CC1: ciphertext component 1 point
 * public input CC2: ciphertext component 2 point
 * private input M: plaintext point
 * private input r: randomness escalar
 *
 * public output C1: ciphertext component 1 point
 * public output C2: ciphertext component 2 point
 */

template ElGamal() {

	signal input Y[2];
	signal input CC1[2];
	signal input CC2[2];
	signal input M[2];	// private
	signal input r;		// private
	signal output C1[2];
	signal output C2[2];

	var B[2] = [
		5299619240641551281634865583518297030282874472190772894086521144482721001553,
		16950150798460657717958625567821834550301663161624707787222815936182638968203
	];
	
	signal preC2[2];
	
	// Convert the randomness to bits
	component rBits = Num2Bits(253);
	rBits.in <== r;
	
	// Compute C1 = r * B
	component rxB = EscalarMulAny(253);
	for (var i = 0; i < 253; i++) {
		rxB.e[i] <== rBits.out[i];
	}
	rxB.p[0] <== B[0];
	rxB.p[1] <== B[1];
	
	C1[0] <== rxB.out[0];
	C1[1] <== rxB.out[1];
	
	// Compute preC2 = r * Y
	component rxY = EscalarMulAny(253);
	for (var i = 0; i < 253; i++) {
		rxY.e[i] <== rBits.out[i];
	}
	rxY.p[0] <== Y[0];
	rxY.p[1] <== Y[1];
	
	preC2[0] <== rxY.out[0];
	preC2[1] <== rxY.out[1];
	
	// Compute C2 = preC2 + M
	component preC2addM = BabyAdd();
	preC2addM.x1 <== preC2[0];
	preC2addM.y1 <== preC2[1];
	preC2addM.x2 <== M[0];
	preC2addM.y2 <== M[1];
	C2[0] <== preC2addM.xout;
	C2[1] <== preC2addM.yout;
	
	// Asserts
	CC1[0] === C1[0];
	CC1[1] === C1[1];
	CC2[0] === C2[0];
	CC2[1] === C2[1];

}

component main {public [Y, CC1, CC2]} = ElGamal();
