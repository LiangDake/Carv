import json
import time

import web3
from web3.middleware import geth_poa_middleware


web3 = web3.Web3(web3.HTTPProvider("https://bsc-dataseed1.binance.org"))

# 连接公共节点需要注入此中间件
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

depositBNB = web3.to_wei(0.03, 'ether')
minGasLimit = 1
extraData = bytes(0)


def multi_transfer(file_name):
    # 读取地址信息
    with open(file_name, 'r') as file:
        # 从文件中加载JSON数据
        wallet_dictionary = json.load(file)
        for wallet in wallet_dictionary:
            transfer_address = wallet['address']
            # 接收钱包地址
            receive_address = '0x865c6f914410ee02ca58d2a94c55db40109ae49b'
            receive_address = web3.to_checksum_address(receive_address)
            nonce = web3.eth.get_transaction_count(transfer_address)
            print(f"{transfer_address} 准备转账")

            transaction = {
                "from": transfer_address,
                "to": receive_address,
                "value": web3.to_wei(0.0269, 'ether'),
                "gas": 25000,
                'gasPrice': web3.to_wei('5', 'gwei'),
                'nonce': nonce
            }

            # 私钥
            private_key = wallet['privateKey']
            signed_transcation = web3.eth.account.sign_transaction(transaction, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_transcation.rawTransaction)
            print(web3.to_hex(tx_hash))
            print(f"{transfer_address} 已转出 {depositBNB} 个BNB")
            time.sleep(5)
            print()


def single_transfer(transfer_address, private_key):
    # 读取地址信息
    transfer_address = web3.to_checksum_address(transfer_address)
    # 接收钱包地址
    receive_address = "0xadc563FcCd94B4f9b8712c21115EFf7eA80dc12E"
    nonce = web3.eth.get_transaction_count(transfer_address)
    print(f"{transfer_address} 准备转账")

    transaction = {
        "from": transfer_address,
        "to": receive_address,
        "value": web3.to_wei(0.0298, 'ether'),
        "gas": 25000,
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': nonce
    }

    signed_transcation = web3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_transcation.rawTransaction)
    print(web3.to_hex(tx_hash))
    print(f"{transfer_address} 已转出 {depositBNB} 个BNB")
    print()


multi_transfer('2024-1-25_mnemonic_address_bot.json')
