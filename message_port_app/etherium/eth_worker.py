import string
import random
import json
import sys
import pprint
from web3.providers.eth_tester import EthereumTesterProvider
from web3 import Web3
from solc import compile_source
from web3.providers.rpc import HTTPProvider
from web3.middleware import geth_poa_middleware
import time
from datetime import datetime

class EthWorker():
    contract_address = '0xfa6f82e8953e3b1a03c274859cdf9f4fbc8b17e5'
    base_address = '0x337DA5Fa7381b1345C273f5702C2Fc1f369e19F0'
    base_pk = '53fc2d4d56d4decaf3afe320e0d12d264574426a9f565f93cb91ba6dc0388745'
    abi_source_path = 'contract_abi.txt'
    #contract_source_path = '/home/maxim/py_yashex_core/message_port_app/etherium/contract.sol'
    w3 = None
    compiled_sol = None
    contract_id = None
    contract_interface = None
    store_var_contract = None
    bargain_id = None

    @staticmethod
    def init_contract():
        #w3 = Web3(EthereumTesterProvider())
        #w3 = Web3(HTTPProvider('http://localhost:8545'))
        EthWorker.w3 = Web3(HTTPProvider('https://rinkeby.infura.io/v3/41da39ce9cfc46cd98721b029811d43f'))
        # inject the poa compatibility middleware to the innermost layer
        EthWorker.w3.middleware_stack.inject(geth_poa_middleware, layer=0)
        compiled_sol = EthWorker.compile_source_file()
        contract_id, contract_interface = compiled_sol.popitem()
        EthWorker.store_var_contract = EthWorker.w3.eth.contract(
            address= EthWorker.w3.toChecksumAddress(EthWorker.contract_address),
            abi=contract_interface['abi'])


    @staticmethod
    def save_bargain_id_and_gen_addr(bargain_id):
        with open("bargain_id.txt", "w") as f:
            f.write(bargain_id)
        EthWorker.generate_keys()
        return EthWorker.get_keys_param('address')

    @staticmethod
    def get_bargain_id():
        f = open("bargain_id.txt", "r")
        result = str(f.read())
        EthWorker.bargain_id = result
        print('get_bargain_id : ' + result)
        return result

    @staticmethod
    def generate_keys():
        from eth_account import Account
        secret = EthWorker.secret_generator()
        acct = Account.create(secret)
        result = '{"secret":"' +str(secret)+ '","private_key":"'+str(acct.privateKey)+'","address":"'+str(acct.address)+'"}'
        with open('keys.json', 'w') as f:
            json.dump(result, f, ensure_ascii=False)
        return str(acct.address)

    @staticmethod
    def get_keys_param(key):
        with open('keys.json') as f:
            f_str = f.read()
            tot_index = f_str.index(':',f_str.index(key))
            result = f_str[ tot_index+4: f_str.index('"',tot_index+3)-1 ]
            print('get_keys_param ' + key +" : "+ result)
        return result

    @staticmethod
    def secret_generator(size=10, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def wait_for_receipt(w3, tx_hash, poll_interval):
        while True:
            tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
            if tx_receipt:
                return tx_receipt
            time.sleep(poll_interval)

    @staticmethod
    def compile_source_file():
        return compile_source(EthWorker.contract)

    @staticmethod
    def getBargainStateById():
        import re
        bargain_id = EthWorker.get_bargain_id()
        if bargain_id is not None:
            print("bargain_id: '" +str(bargain_id) + "'")
            bargain_id = int(re.sub("[^0-9]", "", bargain_id))
            #print('int_bargain_id : '+ bargain_id)
            result = EthWorker.store_var_contract.functions.getBargainStateById(bargain_id).call()
            return result
        else:
            print('bargain_id is none')


    @staticmethod
    def addHistoryItem(message_text):
        bargain_id = int(EthWorker.get_bargain_id())
        timestamp = int(time.mktime(datetime.now().timetuple()))
        gas_estimate = EthWorker.store_var_contract.functions.addHistoryItem(bargain_id, timestamp, 123).estimateGas()


        private_key = EthWorker.get_keys_param('private_key')
        acct = EthWorker.w3.eth.account.privateKeyToAccount(private_key)
        #signed_txn = EthWorker.w3.eth.account.signTransaction(tx, private_key=private_key)
        #EthWorker.w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        print("Gas estimate to transact with setVar: {0}\n".format(gas_estimate))

        if gas_estimate < 100000:
            print("Sending transaction\n")
            tx_hash = EthWorker.store_var_contract.functions.addHistoryItem(bargain_id, timestamp, 123).transact({'from': acct.address,})
            receipt = EthWorker.wait_for_receipt(EthWorker.w3, tx_hash, 1)
            print("Transaction receipt mined: \n")
            pprint.pprint(dict(receipt))
        else:
            print("Gas cost exceeds 100000")



    contract = '''
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
    '''
