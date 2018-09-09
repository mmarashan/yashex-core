from message_port_app.etherium.eth_worker import EthWorker

EthWorker.init_contract()
print("OK init ETHContract")
contract_state = EthWorker.getBargainStateById()
print("contract_state :" + str(contract_state))
EthWorker.addHistoryItem('{I am Ok}')
print("Success adding history item")

