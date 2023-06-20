while getopts f:c:n: flag
do
	case "${flag}" in
		f) folder=${OPTARG};;
		c) ceremony=${OPTARG};;
		n) name=${OPTARG};;
	esac
done

snarkjs groth16 setup $folder/"${name}.r1cs" $ceremony $folder/circuit_0000.zkey
snarkjs zkey contribute $folder/circuit_0000.zkey $folder/circuit_0001.zkey --name="First contribution" -v -e="random entropy"
snarkjs zkey contribute $folder/circuit_0001.zkey $folder/circuit_0002.zkey --name="Second contribution" -v -e="random entropy"
snarkjs zkey contribute $folder/circuit_0002.zkey $folder/circuit_0003.zkey --name="Third contribution" -v -e="random entropy"
snarkjs zkey verify $folder/"${name}.r1cs" $ceremony $folder/circuit_0003.zkey
snarkjs zkey beacon $folder/circuit_0003.zkey $folder/circuit_final.zkey 0123456789 10 -n="Final Beacon phase2"
snarkjs zkey verify $folder/"${name}.r1cs" $ceremony $folder/circuit_final.zkey
snarkjs zkey export verificationkey $folder/circuit_final.zkey $folder/verification_key.json
