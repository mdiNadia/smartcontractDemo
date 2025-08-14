// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VulnerableContract {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function destroy(address payable _recipient) public {
        // بدون بررسی مالکیت → هر کسی می‌تواند کل قرارداد را نابود کند
        selfdestruct(_recipient);
    }
}
