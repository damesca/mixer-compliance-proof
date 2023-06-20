while getopts f:n: flag
do
	case "${flag}" in
		f) folder=${OPTARG};;
		n) name=${OPTARG};;
	esac
done

circom $folder/"${name}.circom" --r1cs --wasm -l ~/mixer-compliance/deps/circomlib/circuits/ -l ~/mixer-compliance/deps/aes-circom/circuits/ -l ~/mixer-compliance/src/circuits/
node $folder/"${name}_js"/generate_witness.js $folder/"${name}_js"/"${name}.wasm" $folder/input.json $folder/witness.wtns
snarkjs wtns check $folder/"${name}.r1cs" $folder/witness.wtns