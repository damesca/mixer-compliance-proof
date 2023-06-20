#!/bin/bash

LIB1=~/mixer-compliance/deps/circomlib/circuits/
LIB2=~/mixer-compliance/deps/aes-circom/circuits/
LIB3=~/mixer-compliance/src/circuits/

usage() {
    echo "Usage: $0 -n circuit_name -f /folder/ [-c ceremony]" >&2; exit 1;
}

witness() {
    circom $folder/"${name}.circom" --r1cs --wasm -l ${LIB1} -l ${LIB2} -l ${LIB3}
    node $folder/"${name}_js"/generate_witness.js $folder/"${name}_js"/"${name}.wasm" $folder/input.json $folder/witness.wtns
    snarkjs wtns check $folder/"${name}.r1cs" $folder/witness.wtns
}

ceremony() {
    snarkjs groth16 setup $folder/"${name}.r1cs" $ceremony $folder/circuit_0000.zkey
    snarkjs zkey contribute $folder/circuit_0000.zkey $folder/circuit_0001.zkey --name="First contribution" -v -e="random entropy"
    snarkjs zkey contribute $folder/circuit_0001.zkey $folder/circuit_0002.zkey --name="Second contribution" -v -e="random entropy"
    snarkjs zkey contribute $folder/circuit_0002.zkey $folder/circuit_0003.zkey --name="Third contribution" -v -e="random entropy"
    snarkjs zkey verify $folder/"${name}.r1cs" $ceremony $folder/circuit_0003.zkey
    snarkjs zkey beacon $folder/circuit_0003.zkey $folder/circuit_final.zkey 0123456789 10 -n="Final Beacon phase2"
    snarkjs zkey verify $folder/"${name}.r1cs" $ceremony $folder/circuit_final.zkey
    snarkjs zkey export verificationkey $folder/circuit_final.zkey $folder/verification_key.json
}

proof() {
    start=`date +%s`
    snarkjs groth16 prove $folder/circuit_final.zkey $folder/witness.wtns $folder/proof.json $folder/public.json
    end=`date +%s`
    runtime=$((end-start))
    echo $runtime
    snarkjs groth16 verify $folder/verification_key.json $folder/public.json $folder/proof.json
}

while getopts "n:f:c:" opt; do
    case $opt in
        n) 
            name=$OPTARG
            ;;
        f) 
            folder=$OPTARG
            ;;
        c) 
            ceremony=$OPTARG
            ;;
        *) 
            usage
            ;;
    esac
done

if [ -z "$name" ] || [ -z "$folder" ]; then
    echo "Missing -n or -f" >&2
    usage
fi

if [ -z "$ceremony" ]; then
    echo "Compute without ceremony"
    echo "Computing the witness..." 
    witness
    echo "Computing the proof..."
    proof
    exit 1;
else
    echo "Compute with ceremony $ceremony"
    echo "Computing the witness..." 
    witness
    echo "Computing the second phase..."
    ceremony
    echo "Computing the proof..."
    proof
    exit 1;
fi