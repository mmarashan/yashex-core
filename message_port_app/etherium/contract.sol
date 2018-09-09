pragma solidity ^0.4.24;

contract Yashchex {
    address superAdmin;
    address[] admins;
    uint constant signaturesTreshold = 2;
    struct HistoryItem {
        uint256 time;
        uint status;
    }

    struct Bargain {
        address seller;
        address buyer;
        address box;
    }

    mapping(uint => Bargain) private bargains;
    mapping(uint => address[]) private bargainSignatures;
    mapping(uint => HistoryItem[]) private bargainHistories;

    constructor() public {
        superAdmin = msg.sender;
    }

    function isAdmin() public view returns (bool) {
        address sender = msg.sender;
        bool res = false;
        for (uint i=0; i<admins.length; i++) {
            if (admins[i] == sender) {
                res = true;
                break;
            }
        }
        return res;
    }

    function addAdmin(address admin) public {
        require(msg.sender == superAdmin);
        admins.push(admin);
    }

    function addBargain(uint id, address seller, address buyer, address box) public {
        bargains[id] = Bargain(seller, buyer, box);
    }

    function addHistoryItem(uint bargainId, uint256 time, uint status) public {
        bargainHistories[bargainId].push(HistoryItem(time, status));
    }

    function getBargainStateById(uint id) view public returns (bool) {
        return bargainSignatures[id].length >= signaturesTreshold ;
    }

    function inArray(address item, address[] array) private pure returns (bool) {
        bool res = false;
        for (uint i=0; i<array.length; i++) {
            if (array[i] == item) {
                res = true;
                break;
            }
        }
        return res;
    }

    function tryToResolveBargain(uint bargainId) public returns (bool) {
        bool res = false;
        address sender = msg.sender;
        address[] storage signatures = bargainSignatures[bargainId];
        if (inArray(sender,signatures)) {
            return res;
        } else {
            bargainSignatures[bargainId].push(sender);
            res = getBargainStateById(bargainId);
        }
        return res;
    }
}