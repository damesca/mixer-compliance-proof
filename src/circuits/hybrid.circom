pragma circom 2.0.0;

include "elgamal_hashed.circom";
//include "elgamal_hashed_mimc.circom";
//include "elgamal_hashed_poseidon.circom";

include "aes_256_ecb_encrypt.circom";

template Hybrid(n_bits) {

	signal input m[n_bits];
	signal input k[256];
	signal input pk[2];
	signal input r;

	signal output c[n_bits];
	signal output tag[256];
	signal output k_C1[2];
	signal output k_c2[256];

	// AES_256_ecb_auth encryption

	component aes_enc = aes_256_ecb_encrypt(n_bits);

	for (var i = 0; i < 256; i++) {
		aes_enc.key[i] <== k[i];
	}
	for (var i = 0; i < n_bits; i++) {
		aes_enc.in[i] <== m[i];
	}
	for (var i = 0; i < n_bits; i++) {
		c[i] <== aes_enc.out[i];
	}
	for (var i = 0; i < 256; i++) {
		tag[i] <== aes_enc.tag[i];
	}

	// ElGamal encryption of k
	component eg = ElGamal_Hashed();

	eg.Y[0] <== pk[0];
	eg.Y[1] <== pk[1];

	for (var i = 0; i < 256; i++) {
		eg.m[i] <== k[i];
	}

	eg.r <== r;

	k_C1[0] <== eg.C1[0];
	k_C1[1] <== eg.C1[1];

	for (var i = 0; i < 256; i++) {
		k_c2[i] <== eg.c2[i];
	}

}