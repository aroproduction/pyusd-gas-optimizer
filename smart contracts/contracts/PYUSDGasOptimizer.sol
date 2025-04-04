// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract PYUSDGasOptimizer is Ownable {
    using SafeERC20 for IERC20;

    IERC20 public pyusd;
    uint256 public minGasPrice;

    struct Transaction {
        address sender;
        address recipient;
        uint256 amount;
        uint256 maxGasPrice;
        bool executed;
    }

    mapping(uint256 => Transaction) public transactions;
    uint256 public transactionCount;

    event TransactionQueued(
        uint256 id,
        address sender,
        address recipient,
        uint256 amount,
        uint256 maxGasPrice
    );
    event TransactionExecuted(uint256 id, uint256 gasPrice);
    event FundsWithdrawn(address sender, uint256 amount);

    constructor(address _pyusd) Ownable(msg.sender) {
        pyusd = IERC20(_pyusd);
        minGasPrice = 10 gwei;
    }

    function queueTransfer(
        address recipient,
        uint256 amount,
        uint256 maxGasPrice
    ) external {
        require(amount > 0, "Amount must be greater than zero");
        require(recipient != address(0), "Invalid recipient");

        pyusd.safeTransferFrom(msg.sender, address(this), amount);

        transactions[transactionCount] = Transaction({
            sender: msg.sender,
            recipient: recipient,
            amount: amount,
            maxGasPrice: maxGasPrice,
            executed: false
        });

        emit TransactionQueued(
            transactionCount,
            msg.sender,
            recipient,
            amount,
            maxGasPrice
        );
        transactionCount++;
    }

    function executeTransaction(uint256 id) external {
        require(id < transactionCount, "Invalid transaction ID");

        Transaction storage txn = transactions[id];
        require(!txn.executed, "Already executed");
        require(txn.sender != address(0), "Invalid sender");

        uint256 currentGasPrice = tx.gasprice;
        require(currentGasPrice <= txn.maxGasPrice, "Gas price too high");
        require(currentGasPrice >= minGasPrice, "Gas price below minimum");

        txn.executed = true;
        pyusd.safeTransfer(txn.recipient, txn.amount);

        emit TransactionExecuted(id, currentGasPrice);
    }

    function batchExecute(uint256[] calldata ids) external {
        require(ids.length <= 50, "Too many transactions");

        uint256 currentGasPrice = tx.gasprice;

        for (uint256 i = 0; i < ids.length; i++) {
            uint256 id = ids[i];
            if (id >= transactionCount) continue;

            Transaction storage txn = transactions[id];
            if (
                !txn.executed &&
                currentGasPrice <= txn.maxGasPrice &&
                currentGasPrice >= minGasPrice
            ) {
                txn.executed = true;
                pyusd.safeTransfer(txn.recipient, txn.amount);
                emit TransactionExecuted(id, currentGasPrice);
            }
        }
    }

    function withdraw(uint256 id) external {
        require(id < transactionCount, "Invalid transaction ID");

        Transaction storage txn = transactions[id];
        require(txn.sender == msg.sender, "Not sender");
        require(!txn.executed, "Already executed");

        txn.executed = true;
        pyusd.safeTransfer(msg.sender, txn.amount);

        emit FundsWithdrawn(msg.sender, txn.amount);
    }

    function setMinGasPrice(uint256 _minGasPrice) external onlyOwner {
        minGasPrice = _minGasPrice;
    }
}
