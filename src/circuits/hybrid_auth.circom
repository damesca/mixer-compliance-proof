pragma circom 2.0.0;

include "elgamal_hashed.circom";
//include "aes_256_ctr_encrypt.circom";
include "aes_256_ecb_encrypt.circom";
include "hmac256.circom";

template Hybrid(n_bits) {

	signal input m[n_bits];
	signal input k[256];
	signal input pk[2];
	signal input r;
	//signal input CC1[2];
	//signal input cc2[256];
	//signal input cc[256];

	signal output c[n_bits];
	signal output tag[256];
	signal output k_C1[2];
	signal output k_c2[256];

	// HMAC
	component hmac = hmac256(n_bits);
	for (var i = 0; i < n_bits; i++) {
		hmac.message[i] <== m[i];
	}
	for (var i = 0; i < 256; i++) {
		hmac.key[i] <== k[i];
	}

	for (var i = 0; i < 256; i++) {
		tag[i] <== hmac.tag[i];
	}

	// AES_256_ctr encryption

	var n[128] = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

	//component aes_enc = AES_256_CTR_ENC(n_bits);
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

	// ElGamal encryption of k
	component eg = ElGamal_Hashed();

	eg.Y[0] <== pk[0];
	eg.Y[1] <== pk[1];

	//eg.CC1[0] <== CC1[0];
	//eg.CC1[1] <== CC1[1];

	for (var i = 0; i < 256; i++) {
		//eg.cc2[i] <== cc2[i];
		eg.m[i] <== k[i];
	}

	eg.r <== r;

	k_C1[0] <== eg.C1[0];
	k_C1[1] <== eg.C1[1];

	for (var i = 0; i < 256; i++) {
		k_c2[i] <== eg.c2[i];
	}

}