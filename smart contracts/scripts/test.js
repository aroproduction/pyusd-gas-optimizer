const hre = require("hardhat");
const ethers = hre.ethers;

async function main() {
  const optimizerAddress = "0xf0e91AA343AA334B94A8Fddcd543C3767396E544";
  const pyusdAddress = "0xcac524bca292aaade2df8a05cc58f0a65b1b3bb9";
  const [user] = await ethers.getSigners();

  const pyusd = await ethers.getContractAt("IERC20", pyusdAddress, user);
  const optimizer = await ethers.getContractAt("PYUSDGasOptimizer", optimizerAddress, user);

  const amount = ethers.parseUnits("10", 6);
  await pyusd.approve(optimizerAddress, amount);
  console.log("Approved 10 PYUSD");

  await optimizer.queueTransfer(user.address, amount, ethers.parseUnits("50", 9));
  console.log("Transfer queued with ID 0");

  const gasPrice = await ethers.provider.getGasPrice();
  console.log("Current gas price:", ethers.formatUnits(gasPrice, "gwei"), "Gwei");

  if (gasPrice.lte(ethers.parseUnits("50", 9))) {
    await optimizer.executeTransaction(0);
    console.log("Transaction executed");
  } else {
    console.log("Gas price too high, waiting...");
  }

  const balance = await pyusd.balanceOf(user.address);
  console.log("Final balance:", ethers.formatUnits(balance, 6), "PYUSD");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
