import json
import time

import cloudscraper
from web3 import Web3

web3 = Web3(Web3.HTTPProvider('https://1rpc.io/eth'))
contract_address = Web3.to_checksum_address("0xE87753eB91D6A61Ea342bB9044A97764366cc7b2")
with open('abi.json', 'r') as abi_file:
    contract_abi = json.load(abi_file)
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

with open('p.txt', 'r') as file:
    private_keys = file.readlines()

mint_num = 2


def get_contract_params(address, num=2):
    scraper = cloudscraper.create_scraper()
    url = 'https://api.tinfun.com/v1/reserve'
    timestamp = int(time.time() * 1000)
    data = {
        "num": num,
        "address": address,
        "timestamp": timestamp
    }
    result = scraper.post(url, json=data)
    print(result.text)
    return result.json()


def interact_with_contract(contract_params, private_key):
    wallet = web3.eth.account.from_key(private_key)
    nonce = web3.eth.get_transaction_count(wallet.address)
    params = contract_params['data']
    tx = contract.functions.publicReserve(
        params['address'], params['number'], params['nonce'], params['sign']
    ).build_transaction({
        'from': wallet.address,
        'value': web3.to_wei(params['number'] * 0.1, 'ether'),
        'gasPrice': web3.eth.gas_price,
        'nonce': nonce,
    })

    es_gas = web3.eth.estimate_gas(tx)
    tx.update({'gas': int(es_gas * 1.1)})
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Transaction hash for {account_address}: {tx_hash.hex()}")
    return tx_hash


# 主程序
if __name__ == '__main__':
    for p in private_keys:
        private_key = p.strip()
        wallet = web3.eth.account.from_key(private_key)
        account_address = wallet.address
        contract_params = get_contract_params(account_address, mint_num)
        interact_with_contract(contract_params, private_key)
