pragma circom 2.0.0;

include "pedersen.circom";
include "hybrid.circom";
include "binsum.circom";
include "bitify.circom";

template tx_compliance_sharing(n) {

    signal input x;
    signal input r;
    signal input x_shares[n];
    signal input r_shares[n];
    signal input mac[2];
    signal input m[128];
    signal input k[256];
    signal input pk[2];
    signal input rand;

    signal output c[128];
    signal output tag[256];
    signal output k_C1[2];
    signal output k_c2[256];

    // Secret reconstruction
    component bitifier_x[n];
    component bitifier_r[n];
    for (var i = 0; i < n; i++) {
        bitifier_x[i] = Num2Bits(256);
        bitifier_r[i] = Num2Bits(256);
        bitifier_x[i].in <== x_shares[i];
        bitifier_r[i].in <== r_shares[i];
    }

    component sum_x = BinSum(256, n);
    component sum_r = BinSum(256, n);
    for (var i = 0; i < n; i++) { //ops
        for (var j = 0; j < 256; j++) { //bits
            sum_x.in[i][j] <== bitifier_x[i].out[j];
            sum_r.in[i][j] <== bitifier_r[i].out[j];
        }
    }

    var nout = nbits((2**256 -1)*n);

    component b2n_x = Bits2Num(nout);
    component b2n_r = Bits2Num(nout);
    for (var i = 0; i < nout; i++) {
        b2n_x.in[i] <== sum_x.out[i];
        b2n_r.in[i] <== sum_r.out[i];
    }

    signal x_rec <== b2n_x.out;
    signal r_rec <== b2n_r.out;

    // Asserts
    
    x_rec === x;
    r_rec === r;
    

    // Commitment
    signal comm[2];
    component ped = pedersen();
    ped.x <== x;
    ped.r <== r;
    comm[0] <== ped.comm[0];
    comm[1] <== ped.comm[1];

    // Asserts
    
    mac[0] === comm[0];
    mac[1] === comm[1];
    

    // Ciphertext
    component cipher = Hybrid(128);
    for (var i = 0; i < 128; i++) {
        cipher.m[i] <== m[i];
    }
    for (var i = 0; i < 256; i++) {
        cipher.k[i] <== k[i];
    }
    cipher.pk[0] <== pk[0];
    cipher.pk[1] <== pk[1];
    cipher.r <== rand;

    for (var i = 0; i < 128; i++) {
        c[i] <== cipher.c[i];
    }

    for (var i = 0; i < 256; i++) {
        tag[i] <== cipher.tag[i];
        k_c2[i] <== cipher.k_c2[i];
    }
    k_C1[0] <== cipher.k_C1[0];
    k_C1[1] <== cipher.k_C1[1];

}