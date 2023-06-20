
while getopts f:n: flag
do
	case "${flag}" in
		f) folder=${OPTARG};;
		n) number=${OPTARG};;
	esac
done

mkdir ./$folder
snarkjs powersoftau new bn128 $number $folder/pot_0000.ptau -v
snarkjs powersoftau contribute $folder/pot_0000.ptau $folder/pot_0001.ptau --name="First contribution" -v -e="some random text"
snarkjs powersoftau contribute $folder/pot_0001.ptau $folder/pot_0002.ptau --name="Second contribution" -v -e="some random text"
snarkjs powersoftau contribute $folder/pot_0002.ptau $folder/pot_0003.ptau --name="Third contribution" -v -e="some random text"
snarkjs powersoftau verify $folder/pot_0003.ptau
snarkjs powersoftau beacon $folder/pot_0003.ptau $folder/pot_beacon.ptau 0123456789 10 -n="Final Beacon"
snarkjs powersoftau prepare phase2 $folder/pot_beacon.ptau $folder/pot_final.ptau -v
snarkjs powersoftau verify $folder/pot_final.ptau

