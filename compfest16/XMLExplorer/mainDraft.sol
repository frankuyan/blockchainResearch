// Create a tool that parses an ethereum public wallet address and returns the balance of the wallet in USD.


pragma solidity ^0.4.0;

contract WalletBalance {
    function getBalance(address _wallet) public view returns (uint) {
        return _wallet.balance;
    }
}


contract WalletBalanceUSD {
    WalletBalance walletBalance = new WalletBalance();
    uint public etherPrice = 1000; // 1 ether = 1000 USD

    function getBalanceUSD(address _wallet) public view returns (uint) {
        return walletBalance.getBalance(_wallet) * etherPrice;
    }
}

// The contract WalletBalanceUSD is a contract that returns the balance of a wallet in USD. It uses the WalletBalance contract to get the balance of the wallet in ether and then multiplies it by the etherPrice to get the balance in USD. The etherPrice is set to 1000 USD per ether in this example.

// To use the WalletBalanceUSD contract, you can call the getBalanceUSD function with the address of the wallet as an argument. This will return the balance of the wallet in USD.

