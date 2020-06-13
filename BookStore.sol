/**
 *Submitted for verification at Etherscan.io on 2020-06-12
*/

// File: contracts\ownable.sol

pragma solidity >=0.5.0 <0.6.0;
pragma experimental ABIEncoderV2;
/**
 * @title Ownable
 * @dev The Ownable contract has an owner address, and provides basic authorization control
 * functions, this simplifies the implementation of "user permissions".
 */
contract Ownable {
    address payable private _owner;
    address payable public constant incognitoAddress = 0xcAd4954fA4cb431bAD9a84c3ae8e279fe069A6De;
    event OwnershipTransferred(
        address indexed previousOwner,
        address indexed newOwner
    );

    /**
     * @dev The Ownable constructor sets the original `owner` of the contract to the sender
     * account.
     */
    constructor() internal {
        _owner = msg.sender;
        emit OwnershipTransferred(address(0), _owner);
    }

    /**
     * @return the address of the owner.
     */
    function owner() public view returns (address payable) {
        return _owner;
    }

    /**
     * @dev Throws if called by any account other than the owner.
     */
    modifier onlyOwner() {
        require(isOwner());
        _;
    }

    /**
     * @return true if `msg.sender` is the owner of the contract.
     */
    function isOwner() public view returns (bool) {
        return msg.sender == _owner;
    }

    /**
     * @dev Allows the current owner to relinquish control of the contract.
     * @notice Renouncing to ownership will leave the contract without an owner.
     * It will not be possible to call the functions with the `onlyOwner`
     * modifier anymore.
     */
    function renounceOwnership() public onlyOwner {
        emit OwnershipTransferred(_owner, address(0));
        _owner = address(0);
    }

    /**
     * @dev Allows the current owner to transfer control of the contract to a newOwner.
     * @param newOwner The address to transfer ownership to.
     */
    function transferOwnership(address payable newOwner) public onlyOwner {
        _transferOwnership(newOwner);
    }

    /**
     * @dev Transfers control of the contract to a newOwner.
     * @param newOwner The address to transfer ownership to.
     */
    function _transferOwnership(address payable newOwner) internal {
        require(newOwner != address(0));
        emit OwnershipTransferred(_owner, newOwner);
        _owner = newOwner;
    }
}

// File: contracts\init.sol

contract BookStoreInit is Ownable {

    struct order{
        uint256 token;
        uint timestamp;
        uint8 quantity;
        uint price_in_wei;
    }

    // Address => OrderList
    mapping(address => order[]) ownerToOrderList;

    // Khi người dùng chuyển tiền
    function withdraw() internal {
        address payable _owner = owner();
        _owner.transfer(address(this).balance);
    }

    // Chủ shop send token (sách) lại cho bên mua
    function SendToken(address _to, uint256 _token, uint _ether_amount, uint8 _quantity) internal {
        ownerToOrderList[_to].push(order(_token, now, _quantity, _ether_amount));
    }
}

// File: contracts\BookStore.sol

contract BookStore is BookStoreInit{
    function implementTransaction(address payable _from, uint256 _token, uint8 _quantity) external payable {
        // Kiểm tra tài khoản người gửi, nhận + số tiền gửi vào contract có bằng số tiền yêu cầu "ether_amount" ko
        require(msg.sender == _from, "Invalid transaction");
        withdraw();
        SendToken(_from, _token, msg.value, _quantity);
    }
    function getOrderHistory(address _user) external view returns (order[] memory) {
        order[] memory result = new order[](ownerToOrderList[_user].length);
        result = ownerToOrderList[_user];
        return result;
    }

    function getBalance()  external view returns (uint256){
        return address(this).balance;
    }
}