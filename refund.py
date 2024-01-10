import json

import cloudscraper
from web3 import Web3

web3 = Web3(Web3.HTTPProvider('https://1rpc.io/eth'))
contract_address = Web3.to_checksum_address("0xE87753eB91D6A61Ea342bB9044A97764366cc7b2")
with open('abi.json', 'r') as abi_file:
    contract_abi = json.load(abi_file)
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

with open('p.txt', 'r') as file:
    private_keys = file.readlines()

max_fee_per_gas = 30


def get_contract_params(address):
    scraper = cloudscraper.create_scraper()
    url = 'https://api.tinfun.com/v1/refund/' + address
    result = scraper.get(url)
    return result.json()


def interact_with_contract(contract_params, private_key):
    wallet = web3.eth.account.from_key(private_key)
    print(f"Address: {wallet.address}")
    nonce = web3.eth.get_transaction_count(wallet.address)
    params = contract_params['data']
    tx = contract.functions.refund(
        params['address'], int(params['refund_balance']), params['nonce'], params['sign']
    ).build_transaction({
        'from': wallet.address,
        'value': 0,
        'maxFeePerGas': web3.to_wei(max_fee_per_gas, 'gwei'),
        'maxPriorityFeePerGas': web3.to_wei(0.1, 'gwei'),
        'nonce': nonce,
    })

    try:
        es_gas = web3.eth.estimate_gas(tx)
        tx.update({'gas': int(es_gas * 1.1)})
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        refund_eth = web3.from_wei(int(params['refund_balance']), 'ether')
        print(f"Transaction hash for {account_address}: https://etherscan.io/tx/{tx_hash.hex()} : refund {refund_eth} ETH")
    except Exception as e:
        print(f"Error during transaction: {e}")
        return None

    return tx_hash


# 主程序
if __name__ == '__main__':
    for p in private_keys:
        try:
            private_key = p.strip()
            wallet = web3.eth.account.from_key(private_key)
            account_address = wallet.address
            contract_params = get_contract_params(account_address)
            interact_with_contract(contract_params, private_key)
        except Exception as e:
            print(f"Error with: {e}")
