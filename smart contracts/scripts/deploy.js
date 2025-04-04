async function main() {
    const GasOptimizer = await ethers.getContractFactory("PYUSDGasOptimizer");
    const optimizer = await GasOptimizer.deploy("0xcac524bca292aaade2df8a05cc58f0a65b1b3bb9");
    await optimizer.waitForDeployment();
    console.log("PYUSDGasOptimizer deployed to:", await optimizer.getAddress());
  }
  
  main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
  });