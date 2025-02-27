#!/bin/bash

LIB1=~/mixer-compliance-proof/deps/circomlib/circuits/
LIB2=~/mixer-compliance-proof/deps/aes-circom/circuits/
LIB3=~/mixer-compliance-proof/src/circuits/
startw=``
endw=``
startp=``
endp=``
runtimew=``
runtimep=``
fulltime=``
timesw=``
timesp=``

usage() {
    echo "Usage: $0 -n circuit_name -f /folder/ [-c ceremony]" >&2; exit 1;
}

compile() {
    date
    /home/daniel/.cargo/bin/circom $folder/"${name}.circom" --r1cs --wasm -l ${LIB1} -l ${LIB2} -l ${LIB3} --output $folder
}

witness() {
    date
    startw=`date +%s%N`
    node $folder/"${name}_js"/generate_witness.js $folder/"${name}_js"/"${name}.wasm" $folder/input.json $folder/witness.wtns
    endw=`date +%s%N`
    
    runtimew=$(((endw-startw)/1000000))
    echo "Witness generation time: ${runtimew}"
    #!snarkjs wtns check $folder/"${name}.r1cs" $folder/witness.wtns
}

ceremony_groth16() {
    date
    snarkjs groth16 setup $folder/"${name}.r1cs" $ceremony $folder/circuit_0000.zkey
    snarkjs zkey contribute $folder/circuit_0000.zkey $folder/circuit_0001.zkey --name="First contribution" -v -e="random entropy"
    snarkjs zkey contribute $folder/circuit_0001.zkey $folder/circuit_0002.zkey --name="Second contribution" -v -e="random entropy"
    snarkjs zkey contribute $folder/circuit_0002.zkey $folder/circuit_0003.zkey --name="Third contribution" -v -e="random entropy"
    #!snarkjs zkey verify $folder/"${name}.r1cs" $ceremony $folder/circuit_0003.zkey
    snarkjs zkey beacon $folder/circuit_0003.zkey $folder/circuit_final.zkey 0123456789 10 -n="Final Beacon phase2"
    #!snarkjs zkey verify $folder/"${name}.r1cs" $ceremony $folder/circuit_final.zkey
    snarkjs zkey export verificationkey $folder/circuit_final.zkey $folder/verification_key.json
}

ceremony_plonk() {
    snarkjs plonk setup $folder/"${name}.r1cs" $ceremony $folder/circuit_final.zkey
    echo "Generating plonk key..."
    snarkjs zkey verify $folder/"${name}.r1cs" $ceremony $folder/circuit_final.zkey
    snarkjs zkey export verificationkey $folder/circuit_final.zkey $folder/verification_key.json
}

proof_groth16() {
    date
    startp=`date +%s%N`
    snarkjs groth16 prove $folder/circuit_final.zkey $folder/witness.wtns $folder/proof.json $folder/public.json
    endp=`date +%s%N`
    runtimep=$(((endp-startp)/1000000))
    echo "Proof generation time: ${runtimep}"
    #!snarkjs groth16 verify $folder/verification_key.json $folder/public.json $folder/proof.json
    date
}

proof_plonk() {
    startp=`date +%s%N`
    snarkjs plonk prove $folder/circuit_final.zkey $folder/witness.wtns $folder/proof.json $folder/public.json
    endp=`date +%s%N`
    runtimep=$(((endp-startp)/1000000))
    echo "Proof generation time: ${runtimep}"
    snarkjs plonk verify $folder/verification_key.json $folder/public.json $folder/proof.json
}

showtime() {
    fulltime=$((runtimew+runtimep))
    echo "Witness generation time: ${runtimew}"
    echo "Proof generation time: ${runtimep}"
    echo "Full time: ${fulltime}"
    timesw+="${runtimew},"
    timesp+="${runtimep},"
    echo "---------- END ----------"
}

while getopts "n:f:p:c:" opt; do
    case $opt in
        n) 
            name=$OPTARG
            ;;
        f) 
            folder=$OPTARG
            ;;
        p)
            protocol=$OPTARG
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
    if [ "$protocol" = "plonk" ]; then
        echo "Compute without ceremony"
        echo "Computing the witness..." 
        compile
        witness
        echo "Computing the proof..."
        proof_plonk
        showtime
        exit 1;
    else 
        for x in {1..25}
        do
            echo "Compute without ceremony"
            echo "Computing the witness..." 
            compile
            witness
            echo "Computing the proof..."
            proof_groth16
            showtime
        done
        echo "witness: ${timesw}"
        echo "proof: ${timesp}"
        exit 1;
    fi
else
    if [ "$protocol" = "plonk" ]; then
        echo "Compute with ceremony $ceremony"
        echo "Computing the witness..." 
        compile
        witness
        echo "Computing the second phase..."
        ceremony_plonk
        echo "Computing the proof..."
        proof_plonk
        showtime
        exit 1;
    else
        echo "Compute with ceremony $ceremony"
        echo "Compiling circuit..."
        compile
        echo "Computing the second phase..."
        ceremony_groth16
        echo "Computing the witness..." 
        witness
        echo "Computing the proof..."
        proof_groth16
        showtime
        exit 1;
    fi
fi