require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

module.exports = {
  solidity: "0.8.20",
  networks: {
    sepolia: {
      url: process.env.GCP_RPC,
      accounts: [process.env.PRIVATE_KEY]
    }
  }
};