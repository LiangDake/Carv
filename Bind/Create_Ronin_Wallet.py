import json
from eth_account import Account
from mnemonic import Mnemonic

# 启用未经审核的 HD 钱包功能
Account.enable_unaudited_hdwallet_features()


def generate_ronin_wallets(n):
    wallets = []
    mnemo = Mnemonic("english")
    for _ in range(n):
        # 生成助记词
        mnemonic = mnemo.generate(strength=256)

        # 使用助记词创建钱包
        acct = Account.from_mnemonic(mnemonic)

        # 生成钱包信息
        wallet = {
            "mnemonic": mnemonic,  # 助记词
            "address": acct.address,  # 钱包地址
            "private_key": acct.key.hex()  # 私钥
        }
        wallets.append(wallet)
    return wallets


def save_wallets_to_json(wallets, filename='ronin_wallets.json'):
    with open(filename, 'w') as file:
        json.dump(wallets, file, indent=4)
    print(f"Wallets saved to {filename}")


# 批量生成指定数量的 Ronin 钱包
number_of_wallets = 10  # 你想生成的钱包数量
wallets = generate_ronin_wallets(number_of_wallets)

# 将生成的钱包信息保存到 JSON 文件
save_wallets_to_json(wallets)
