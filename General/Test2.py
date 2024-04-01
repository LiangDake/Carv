# from web3 import Web3
#
# # RPC URL，你需要替换成opBNB的RPC URL
# rpc_url = "https://opbnb-mainnet.nodereal.io/v1/24a9a79ff7ce4606a8f5e6dc2bfe7dbe"
#
# # 创建Web3连接
# w3 = Web3(Web3.HTTPProvider(rpc_url))
#
# # 钱包地址，替换为你想查询的地址
# address = "0x8e9Af756530807813B3D2f4fca564161a9B44BCe"
#
# # 获取交易计数，这也表示该地址发出的交易总数
# nonce = w3.eth.get_transaction_count(address)
#
# if nonce == 0:
#     print("该地址没有发出任何交易。")
# else:
#     # 对于获取第一条交易记录，你可能需要遍历交易历史，这在二层链中可能比较复杂，因为不是所有RPC节点都支持所有查询类型
#     # 这里提供一个基本思路：查看账户的交易历史来尝试找到最早的交易
#     print(f"该地址发出的交易总数为：{nonce}")
#     # 进一步的操作依赖于opBNB链对交易历史查询的支持情况

from web3 import Web3

# 初始化Web3对象并连接到区块链节点
w3 = Web3(Web3.HTTPProvider("https://opbnb-mainnet.nodereal.io/v1/24a9a79ff7ce4606a8f5e6dc2bfe7dbe"))

# 替换下面的字符串为你想查询的交易哈希值
transaction_hash = '0xac5190ed37a3c779d554930fd0843ee59e75aa2fe184499d6f80b60c0d33c21b'

# 使用Web3获取交易信息
transaction = w3.eth.get_transaction(transaction_hash)

if transaction:
    print(f"交易详情: {transaction}")
else:
    print("未找到该交易。")

input_hex = Web3.to_hex(transaction['input'])
print(input_hex)

# 地址部分从第26个字符开始，到第66个字符结束
address_hex = input_hex[10:74]  # 截取地址部分的十六进制字符串

# 确保地址字符串以0x开始
address_hex_with_prefix = "0x" + address_hex[-40:]  # 保证只取后40个字符

# 使用Web3将字符串转换为以太坊的校验和地址格式
address = Web3.to_checksum_address(address_hex_with_prefix)

print(address)

