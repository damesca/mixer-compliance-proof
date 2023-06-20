pragma circom 2.0.0;

include "escalarmulfix.circom";
include "escalarmulany.circom";
include "bitify.circom";
include "babyjub.circom";
include "poseidon.circom";

/*
 * Encrypts an ElGamal ciphertext with BabyJubJub EC in twisted edw form
 *
 * public input Y: public key point
 * public input CC1: ciphertext component 1 point
 * public input CC2: ciphertext component 2 point
 * private input m: plaintext (bits)
 * private input r: randomness escalar
 *
 * public output C1: ciphertext component 1 point
 * public output c2: ciphertext component 2 (bits)
 */

template ElGamal_Hashed() {

	signal input Y[2];
	signal input m[256];	// private
	signal input r;		    // private

	signal output C1[2];
	signal output c2[256];

	signal preC2[2];

	// Baby Jub Jub base point (twisted Edwards form)
	var B[2] = [
		5299619240641551281634865583518297030282874472190772894086521144482721001553,
		16950150798460657717958625567821834550301663161624707787222815936182638968203
	];
	
	// Convert the randomness to bits
	component rBits = Num2Bits(256);
	rBits.in <== r;
	
	// Compute C1 = r * B
	component r_times_B = EscalarMulFix(256, B);
	for (var i = 0; i < 256; i++) {
		r_times_B.e[i] <== rBits.out[i];
	}
	
	C1[0] <== r_times_B.out[0];
	C1[1] <== r_times_B.out[1];

	// Compute preC2 = r * Y
	component r_times_Y = EscalarMulAny(256);
	for (var i=0; i<256; i++) {
		r_times_Y.e[i] <== rBits.out[i];
	}
	r_times_Y.p[0] <== Y[0];
	r_times_Y.p[1] <== Y[1];

    component hash = Poseidon(2);
    hash.inputs[0] <== r_times_Y.out[0];
    hash.inputs[1] <== r_times_Y.out[1];

    signal xor[256];
    component bitify_hash = Num2Bits(256);
    bitify_hash.in <== hash.out;
    for (var i = 0; i < 256; i++) {
        xor[i] <-- bitify_hash.out[i] ^ m[i];
        c2[i] <== xor[i];
    }


}