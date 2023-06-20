const zkSnark = require("snarkjs");
const wasmTester = require("circom_tester").wasm;
const path = require("path");
const logCreator = require("logplease");

const logger = logCreator.create("snarkJS", {showTimestamp: false});

async function witness() {
	console.log(zkSnark);
	const circuit = await wasmTester(path.join(__dirname, "circuit.circom"))
	//console.log(circuit);
	const w = await circuit.calculateWitness({a: 2, b: 4});
	//console.log(w);
	//console.log(await circuit.checkConstraints(w));
	const acc = await zkSnark.powersOfTau.newAccumulator("BN128", 8, "pot8.ptau", logger);
	console.log(acc);
}

witness().then(() => {
	console.log("Computed witness...");
	process.exit(0);
});
