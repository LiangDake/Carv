import json

from mnemonic import Mnemonic
from solana.rpc.api import Client


def generate_solana_wallets(n):
    wallets = []
    mnemo = Mnemonic("english")
    for _ in range(n):
        # 生成助记词
        mnemonic = mnemo.generate(strength=128)

        # 从助记词生成种子，然后从种子的前32字节生成密钥对
        seed = Mnemonic.to_seed(mnemonic)[:32]

        # 生成钱包信息
        wallet = {
            "mnemonic": mnemonic,  # 助记词
        }
        wallets.append(wallet)
    return wallets


def save_wallets_to_json(wallets, filename='solana_wallets.json'):
    with open(filename, 'w') as file:
        json.dump(wallets, file, indent=4)
    print(f"Wallets saved to {filename}")


# 批量生成指定数量的Solana钱包
number_of_wallets = 10  # 你想生成的钱包数量
wallets = generate_solana_wallets(number_of_wallets)

# 将生成的钱包信息保存到 JSON 文件
save_wallets_to_json(wallets)
