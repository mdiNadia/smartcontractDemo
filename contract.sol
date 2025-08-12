// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DemoGraph {
    uint256 public data;

    function start(uint256 x) public {
        setData(x);
    }

    function setData(uint256 x) public {
        data = x;
        process();
    }

    function process() internal {
        helper();
    }

    function helper() internal {
        // اینجا عمداً یک حلقه تماس ایجاد می‌کنیم
        check();
    }

    function check() internal {
        if (data > 10) {
            helper(); // ایجاد cycle
        }
    }

    function externalCallExample(address payable target) public {
        target.transfer(1 ether); // تست external call
    }
}
