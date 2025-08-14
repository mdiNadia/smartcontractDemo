// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VulnerableBank {
    mapping(address => uint) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw() public {
        uint amount = balances[msg.sender];
        require(amount > 0, "No balance");
        // ارسال قبل از صفر کردن موجودی → آسیب‌پذیری
        (bool success,) = msg.sender.call{value: amount}("");
        require(success, "Failed");
        balances[msg.sender] = 0;
    }
}
