import json
from web3 import Web3
import time
import random
from termcolor import cprint

time_ot = 15
time_do = 20

# RPCs
polygon_rpc_url = 'https://polygon-rpc.com/'
w3 = Web3(Web3.HTTPProvider(polygon_rpc_url))
# ABIs
abi = json.load(open('rari_abi.json'))

nft_address = w3.to_checksum_address('0x8e0dcca4e6587d2028ed948b7285791269059a62')
nft_contract = w3.eth.contract(address=nft_address, abi=abi) # бридж


with open("privates.txt", "r") as f:
    keys_list = [row.strip() for row in f if row.strip()]
    numbered_keys = list(enumerate(keys_list, start=1))
    random.shuffle(numbered_keys)

for wallet_number, PRIVATE_KEY in numbered_keys:
    account = w3.eth.account.from_key(PRIVATE_KEY)
    address = account.address
    matic_balance = w3.eth.get_balance(address)
    matic = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
    proof = '0x0000000000000000000000000000000000000000000000000000000000000000'

    print(time.strftime("%H:%M:%S", time.localtime()))
    print(f'[{wallet_number}] - {address}', flush=True)

    print('Баланс MATIC:', matic_balance / 10 ** 18)


    gasPrice = w3.eth.gas_price
    gas = random.randint(200940, 231940)  # c каким газлимитом уйдет транза

    maxFeePerGas = random.randint(179795965109, 199795965109)

    swap_txn = nft_contract.functions.claim(address, 1, matic, 0,([proof],1,0, matic), '0x').build_transaction({
        'from': address,
        'maxFeePerGas': maxFeePerGas,
        'maxPriorityFeePerGas': w3.to_wei(30, 'gwei'),
        'nonce': w3.eth.get_transaction_count(address),
        'gas': gas,
    })

    try:

        signed_swap_txn = w3.eth.account.sign_transaction(swap_txn, PRIVATE_KEY)
        swap_txn_hash = w3.eth.send_raw_transaction(signed_swap_txn.rawTransaction)
        print(f"Transaction: https://polygonscan.com/tx/{swap_txn_hash.hex()}")
        cprint("Вроде бы норм", "green")
        time.sleep(random.randint(time_ot, time_do))

    except:
        cprint("Что то пошло не так", "red")







