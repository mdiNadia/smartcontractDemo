// SPDX-License-Identifier: MIT
pragma solidity ^0.4.24;  // نسخه‌ای که parser بدون مشکل پشتیبانی کند

contract VulnerableBank {
    mapping(address => uint) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw() public {
        uint amount = balances[msg.sender];
        require(amount > 0);

        // آسیب‌پذیری: ارسال قبل از صفر کردن موجودی
        if (!msg.sender.send(amount)) {
            revert();
        }

        balances[msg.sender] = 0;
    }
}
