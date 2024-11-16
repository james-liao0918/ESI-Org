// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ESICoin {
    // Basic token details
    string public name = "ESI Coin";
    string public symbol = "ESIC";
    uint8 public decimals = 18;
    uint256 public totalSupply;

    // Admin address
    address public admin;

    // Balances and exempt account mappings
    mapping(address => uint256) public balances;
    mapping(address => bool) public exemptAccounts;

    // Events for transparency
    event Transfer(address indexed sender, address indexed receiver, uint256 amount, uint256 fee);
    event Mint(address indexed account, uint256 amount);
    event ExemptAccountAdded(address indexed account);
    event ExemptAccountRemoved(address indexed account);

    constructor() {
        admin = msg.sender; // Set contract deployer as the admin
    }

    // Modifier to restrict functions to admin
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    /**
     * Mint new tokens for an account.
     * Only admin can call this function.
     */
    function mint(address account, uint256 amount) external onlyAdmin {
        require(account != address(0), "Invalid account address");
        totalSupply += amount;
        balances[account] += amount;
        emit Mint(account, amount);
    }

    /**
     * Add an exempt account (no fees applied to transactions).
     * Only admin can call this function.
     */
    function setExemptAccount(address account, bool isExempt) external onlyAdmin {
        require(account != address(0), "Invalid account address");
        exemptAccounts[account] = isExempt;

        if (isExempt) {
            emit ExemptAccountAdded(account);
        } else {
            emit ExemptAccountRemoved(account);
        }
    }

    /**
     * Transfer tokens between accounts with optional fee deduction.
     */
    function transfer(address receiver, uint256 amount) external returns (bool success) {
        require(receiver != address(0), "Invalid receiver address");
        require(balances[msg.sender] >= amount, "Insufficient balance");

        uint256 fee = 0;

        // Check if sender is exempt from fees
        if (!exemptAccounts[msg.sender]) {
            fee = calculateFee(amount);
        }

        uint256 amountAfterFee = amount - fee;

        // Deduct from sender and add to receiver
        balances[msg.sender] -= amount;
        balances[receiver] += amountAfterFee;

        // Emit the transfer event
        emit Transfer(msg.sender, receiver, amountAfterFee, fee);
        return true;
    }

    /**
     * Calculate the fee for a transaction.
     * Example logic: 0.5% fee.
     */
    function calculateFee(uint256 amount) internal pure returns (uint256) {
        return (amount * 5) / 1000;
    }
}
