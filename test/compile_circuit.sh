while getopts f:n: flag
do
	case "${flag}" in
		f) folder=${OPTARG};;
		n) name=${OPTARG};;
	esac
done

/home/daniel/.cargo/bin/circom $folder/"${name}.circom" --r1cs --wasm -l /home/daniel/mixer-compliance-proof/deps/circomlib/circuits/ -l /home/daniel/mixer-compliance-proof/deps/aes-circom/circuits/ -l /home/daniel/mixer-compliance-proof/src/circuits/
node $folder/"${name}_js"/generate_witness.js $folder/"${name}_js"/"${name}.wasm" $folder/input.json $folder/witness.wtns
snarkjs wtns check $folder/"${name}.r1cs" $folder/witness.wtns