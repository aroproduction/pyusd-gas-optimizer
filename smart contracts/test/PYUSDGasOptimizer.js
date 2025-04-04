const { expect } = require("chai");

describe("PYUSDGasOptimizer", function () {
    it("Should queue and execute a transfer", async function () {
        const [owner, user] = await ethers.getSigners();
        const PYUSD = await ethers.getContractFactory("ERC20Mock"); // Mock PYUSD
        const pyusd = await PYUSD.deploy("PYUSD", "PYUSD", ethers.utils.parseEther("1000"));
        await pyusd.deployed();

        const GasOptimizer = await ethers.getContractFactory("PYUSDGasOptimizer");
        const optimizer = await GasOptimizer.deploy(pyusd.address);
        await optimizer.deployed();

        await pyusd.connect(user).approve(optimizer.address, ethers.utils.parseEther("100"));
        await optimizer.connect(user).queueTransfer(user.address, ethers.utils.parseEther("50"), 50e9); // 50 Gwei
        await optimizer.executeTransaction(0);
        expect(await pyusd.balanceOf(user.address)).to.equal(ethers.utils.parseEther("950")); // Initial 1000 - 50
    });
});