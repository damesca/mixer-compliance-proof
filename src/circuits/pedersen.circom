pragma circom 2.0.0;

include "escalarmulfix.circom";
include "babyjub.circom";

template pedersen() {

    signal input x;
    signal input r;

    signal output comm[2];

    // Baby Jub Jub base point (twisted Edwards form)
	var B[2] = [
		5299619240641551281634865583518297030282874472190772894086521144482721001553,
		16950150798460657717958625567821834550301663161624707787222815936182638968203
	];

    component xBits = Num2Bits(256);
    component rBits = Num2Bits(256);

    xBits.in <== x;
    rBits.in <== r;

    component x_times_B = EscalarMulFix(256, B);
    component r_times_B = EscalarMulFix(256, B);

    for (var i = 0; i < 256; i++) {
        x_times_B.e[i] <== xBits.out[i];
        r_times_B.e[i] <== rBits.out[i];
    }

    component adder = BabyAdd();
    adder.x1 <== x_times_B.out[0];
    adder.y1 <== x_times_B.out[1];
    adder.x2 <== r_times_B.out[0];
    adder.y2 <== r_times_B.out[1];

    comm[0] <== adder.xout;
    comm[1] <== adder.yout;

}