pragma circom 2.0.0;

include "hybrid.circom";

/*
 * Proves that a linkage param fulfils compliance requirements,
 * according to a decryption mixnet-based mixer
 *
 * Public input l: linkage param
 * Public input cm: Message encrypted with the mixnet keys
 * Public input PK[n]: List of mixnet public keys
 * Public input PK_reg: Regulator's public key
 * Private input k: Regulator's encryption symmetric key
 * Private input m: Message sent, where m = (Enc_l || o)
 * Private input Enc_l: linkage param encrypted with PK_reg
 * Private input o: receiver's address
 * Private input r_l: randomness used to encrypt l
 * Private input r[n]: randomness used to encrypt the message for the mixnet
 * Private input k[n]: symmetric key for encryption
 */
 
 template Compliance(rounds) {

	var m_len = 128;
	var a_len = 256;
	var len = m_len + a_len;
 
 	signal input l[m_len];
	signal input k_reg[256];
	signal input pk_reg[2];
	signal input rand_reg;

	signal input l_ctxt[m_len];
	signal input l_tag[256];
	signal input l_c1[2];
	signal input l_c2[256];

	signal input address[a_len];

	signal input k[rounds][256];
	signal input pk[rounds][2];
	signal input rand[rounds];

	signal input inpt_ctxt[len];
	signal input inpt_eg_c1[rounds][2];
	signal input inpt_eg_c2[rounds][256];

	signal output ctxt[len];
	signal output eg_c1[rounds][2];
	signal output eg_c2[rounds][256];
	signal output tags[rounds][256];

 	// Encrypt l with regulator's key
 	
 	component h_reg = Hybrid(m_len);
 	for(var i = 0; i < m_len; i++) {
		h_reg.m[i] <== l[i];
	}
	for(var i = 0; i < 256; i++) {
		h_reg.k[i] <== k_reg[i];
	}
	h_reg.pk[0] <== pk_reg[0];
	h_reg.pk[1] <== pk_reg[1];
	h_reg.r <== rand_reg;

	// Asserts
	/*
	for(var i = 0; i < m_len; i++) {
		l_ctxt[i] === h_reg.c[i];
	}
	l_c1[0] === h_reg.k_C1[0];
	l_c1[1] === h_reg.k_C1[1];
	for(var i = 0; i < 256; i++) {
		l_c2[i] === h_reg.k_c2[i];
		l_tag[i] === h_reg.tag[i];
	}
	*/

	// Create message for mixnet
	
	signal m[len];
	for(var i = 0; i < m_len; i++) {
		m[i] <== h_reg.c[i];
	}
	for(var i = 0; i < a_len; i++) {
		m[i + m_len] <== address[i];
	}

	// Sequential encryption
	component h_enc[rounds];
 	for (var i = 0; i < rounds; i++) {
		h_enc[i] = Hybrid(len);
	}
 	
	signal ptxt[rounds+1][len];
	for(var i = 0; i < len; i++) {
		ptxt[0][i] <== m[i];
	}
 	
	for (var i = 0; i < rounds; i++) {

		for(var j = 0; j < len; j++) {
			h_enc[i].m[j] <== ptxt[i][j];
		}
		for(var j = 0; j < 256; j++) {
			h_enc[i].k[j] <== k[i][j];
		}
		h_enc[i].pk[0] <== pk[i][0];
		h_enc[i].pk[1] <== pk[i][1];
		h_enc[i].r <== rand[i];
		for(var j = 0; j < len; j++) {
			ptxt[i+1][j] <== h_enc[i].c[j];
		}
		eg_c1[i][0] <== h_enc[i].k_C1[0];
		eg_c1[i][1] <== h_enc[i].k_C1[1];
		for(var j = 0; j < 256; j++) {
			eg_c2[i][j] <== h_enc[i].k_c2[j];
			tags[i][j] <== h_enc[i].tag[j];
		}
	}

	for(var i = 0; i < len; i++) {
		ctxt[i] <== ptxt[rounds][i];
	}

	// Asserts
	/*
	signal one <== 1;
	for(var i = 0; i < len; i++) {
		ctxt[i] === (inpt_ctxt[i] * one);
	}
	for(var i = 0; i < rounds; i++) {
		eg_c1[i][0] === (inpt_eg_c1[i][0] * one);
		eg_c1[i][1] === (inpt_eg_c1[i][1] * one);
		for(var j = 0; j < 256; j++) {
			eg_c2[i][j] === (inpt_eg_c2[i][j] * one);
		}
	}
	*/
	
 }
 
 //component main {public [l, cm, PK, PK_reg]} = Compliance(2);