pragma circom 2.0.0;

include "escalarmulfix.circom";

template testEscalarMul() {

    var B[2] = [
        5299619240641551281634865583518297030282874472190772894086521144482721001553,
        16950150798460657717958625567821834550301663161624707787222815936182638968203
    ];
    var P[2] = [
        17777552123799933955779906779655732241715742912184938656739573121738514868268,
        2626589144620713026669568689430873010625803728049924121243784502389097019475
    ];
    var n = 2;
    signal input e;
    //signal input P[2];
    signal output Q[2];

    component bitifier = Num2Bits(n);
    bitifier.in <== e;

    component multiplier = EscalarMulFix(n, P);
    for (var i=0; i<n; i++) {
        multiplier.e[i] <== bitifier.out[i];
    }
    //multiplier.inp[0] <== P[0];
    //multiplier.inp[1] <== P[1];
    Q[0] <== multiplier.out[0];
    Q[1] <== multiplier.out[1];

}

component main = testEscalarMul();