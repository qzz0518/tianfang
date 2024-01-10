import cloudscraper
from web3 import Web3

web3 = Web3(Web3.HTTPProvider('https://1rpc.io/eth'))

with open('p.txt', 'r') as file:
    private_keys = file.readlines()


def query(address):
    scraper = cloudscraper.create_scraper()
    url = 'https://api.tinfun.com/v1/ticket/' + address
    result = scraper.get(url)
    data = result.json()
    for ticket in data['data']['tickets']:
        if ticket['win']:
            print(f"{address} 发财了! 中奖编号: {ticket['number']}")


if __name__ == '__main__':
    for p in private_keys:
        try:
            private_key = p.strip()
            wallet = web3.eth.account.from_key(private_key)
            account_address = wallet.address
            contract_params = query(account_address)
        except Exception as e:
            print(f"Error with: {e}")
