pragma circom 2.0.0;

include "bitify.circom";

template Concat(n) {

	signal input a;
	signal input b;
	signal output c;

	component num2bits_a = Num2Bits(n);
	num2bits_a.in <== a;
	signal a_bits[n] <== num2bits_a.out;
	
	component num2bits_b = Num2Bits(n);
	num2bits_b.in <== b;
	signal b_bits[n] <== num2bits_b.out;
	
	signal c_bits[n+n];
	for (var i = 0; i < n; i++) {
		c_bits[i] <== a_bits[i];
		c_bits[i+n] <== b_bits[i];
	}

	component bits2num = Bits2Num(n+n);
	bits2num.in <== c_bits;
	c <== bits2num.out;

}

