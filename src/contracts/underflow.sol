// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract OverflowToken {
    mapping(address => uint256) public balances;

    constructor() public {
        balances[msg.sender] = 100;
    }

    function transfer(address _to, uint256 _amount) public {
        require(balances[msg.sender] >= _amount, "Not enough tokens");
        balances[msg.sender] -= _amount;
        balances[_to] += _amount; // اگر overflow شود، مقدار برمی‌گردد به صفر
    }
}
