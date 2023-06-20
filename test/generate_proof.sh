while getopts f:n: flag
do
	case "${flag}" in
		f) folder=${OPTARG};;
	esac
done

snarkjs groth16 prove $folder/circuit_final.zkey $folder/witness.wtns $folder/proof.json $folder/public.json
snarkjs groth16 verify $folder/verification_key.json $folder/public.json $folder/proof.json