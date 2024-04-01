import csv
import time
from web3.middleware import geth_poa_middleware
from telnetlib import EC
from selenium.webdriver import ActionChains
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from General.bit_api import *
import random
import string
import pyperclip
from General.bit_api import openBrowser
import web3

web3 = web3.Web3(web3.HTTPProvider("https://opbnb-mainnet-rpc.bnbchain.org"))
# 连接公共节点需要注入此中间件
web3.middleware_onion.inject(geth_poa_middleware, layer=0)


# 网页元素基本操作
def element_input(path, content):  # 填入您需要操作的元素的路径以及内容
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, path))).send_keys(content)


def element_click(path):  # 填入您需要操作的元素的路径
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, path))).click()


def is_element_displayed(path):
    attempt = 5
    result = False
    while attempt > 0:
        try:
            driver.find_element(By.XPATH, path)
        except Exception:
            attempt -= 1
            time.sleep(1)
        else:
            result = True
            break
    return result


def is_element_displayed_in_2s(path):
    attempt = 2
    result = False
    while attempt > 0:
        try:
            driver.find_element(By.XPATH, path)
        except Exception:
            attempt -= 1
            time.sleep(1)
        else:
            result = True
            break
    return result


def web_jump_new():
    attempt = 5
    new_window_handle = None
    former_web = driver.current_window_handle
    while not new_window_handle and attempt > 0:
        for handle in driver.window_handles:
            if handle != former_web:
                new_window_handle = handle
        attempt -= 1
        time.sleep(1)
    driver.switch_to.window(new_window_handle)
    return former_web


# 跳转至指定页面
def web_jump_to(handle):
    driver.switch_to.window(handle)


def web_scroll(path):  # 滚动到某个元素的位置
    element = driver.find_element(By.XPATH, path)
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(2)


def import_private_key(file_name):
    with open(file_name, 'r') as file:
        # 从文件中加载JSON数据
        wallet_dictionary = json.load(file)
        wallet_number = 0
        for wallet in wallet_dictionary:
            private_key = wallet['privateKey']
            # Account1
            element_click('//*[@id="app-content"]/div/div[2]/div/button')
            # + Add account or hardware wallet
            element_click('/html/body/div[3]/div[3]/div/section/div[4]/button')
            # 导入账户
            element_click('/html/body/div[3]/div[3]/div/section/div[2]/div[2]/button')
            # 粘贴私钥
            element_input('//*[@id="private-key-box"]', private_key)
            # 导入
            element_click('/html/body/div[3]/div[3]/div/section/div[2]/div/div[2]/button[2]')
            wallet_number += 1
            print(f"{wallet['address']} 已导入至钱包，目前共 {wallet_number} 个钱包")
        print()
        print(f"{wallet_number} 个钱包已导入。")


def choose_wallet(number):
    action_chains = ActionChains(driver)
    # Account Button
    element_click('//*[@id="app-content"]/div/div[2]/div/button')
    # 滚动至第一个使用的账号位置
    path = "//*[contains(text(),'Account " + str(number) + "')]"
    # 点击切换账号
    is_element_displayed(path)
    element_click(path)



def account_upload(csv_file_name, account_list):
    with open(csv_file_name, 'a', newline='') as f:
        # Create a dictionary writer with the dict keys as column fieldnames
        writer = csv.DictWriter(f, fieldnames=account_list.keys())
        # Append single row to CSV
        writer.writerow(account_list)


def single_transfer(transfer_address, private_key, receive_address):
    print("即将开始转账")
    # 读取地址信息
    transfer_address = web3.to_checksum_address(transfer_address)
    nonce = web3.eth.get_transaction_count(transfer_address)
    print(f"{transfer_address} 准备转账")

    transaction = {
        "from": transfer_address,
        "to": receive_address,
        "value": web3.to_wei(0.0023, 'ether'),
        "gas": 25000,
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': nonce
    }

    signed_transcation = web3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_transcation.rawTransaction)
    print(web3.to_hex(tx_hash))
    print(f"{transfer_address} 已转出 {web3.to_wei(0.0023, 'ether')} 个BNB至 {receive_address}")
    print()


# 执行代码前确保主账号邀请链接正确
if __name__ == '__main__':
    # 初始化
    res = openBrowser('fb4694579e4048729d3ea86de12c7b8a')  # 比特浏览器窗口ID
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", res['data']['http'])
    service = Service(executable_path=res['data']['driver'])

    # 第一个钱包的编号
    wallet_number = 5
    last_wallet_number = 107
    while wallet_number <= last_wallet_number:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
        # 小狐狸钱包切换账号
        choose_wallet(wallet_number)
        time.sleep(0.5)
        # 进入Carv界面
        driver.get('https://protocol.carv.io/airdrop?invite_code=AU7QF2')
        time.sleep(2)
        # 跳转至小狐狸
        former_web = web_jump_new()
        # 签名
        element_click('//*[@id="app-content"]/div/div/div/div[4]/footer/button[2]')
        time.sleep(1)
        driver.switch_to.window(former_web)
        driver.refresh()
        time.sleep(2)
        service_path = "//*[contains(text(),'.Play Name Service')]"
        element_click(service_path)
        # Generate a 10-character random string including lowercase letters, digits, and '-'
        chars = string.ascii_lowercase + string.digits + '-'
        random_string_lower = ''.join(random.choice(chars) for _ in range(20))
        # 随机输入字符串
        element_input('//*[@id="handle"]', random_string_lower)
        time.sleep(1)
        if is_element_displayed(
                '/html/body/div[3]/div[3]/div/div[2]/div/div/div[1]/form/div[2]/div[2]/button'):
            # 点击Mint
            element_click('/html/body/div[3]/div[3]/div/div[2]/div/div/div[1]/form/div[2]/div[2]/button')
            time.sleep(10)
            # 跳转小狐狸
            former_web = web_jump_new()
            time.sleep(2)
            confirm_path = '//*[@id="app-content"]/div/div/div/div[3]/div[3]/footer/button[2]'
            while True:
                try:
                    element_click(confirm_path)
                    break
                except Exception:
                    time.sleep(0.5)
            # 等待Mint成功自动跳转
            time.sleep(20)
            web_jump_to(former_web)
            time.sleep(2)
            # 成功后进行下一个账号
            print(f"Account {wallet_number} 域名绑定成功，即将进行下一个")
            print()
            # Free Mint
            carv_path = "//*[contains(text(),'Free CARV')]"
            if is_element_displayed(carv_path):
                element_click(carv_path)
                time.sleep(1)
                if is_element_displayed('/html/body/div[3]/div[3]/div/div[2]/div/div[2]/button'):
                    element_click('/html/body/div[3]/div[3]/div/div[2]/div/div[2]/button')
                    time.sleep(1)
                    # 成功后进行下一个账号
                    print(f"Account {wallet_number} Free Mint成功，即将进行下一个")
                    print()
                    # opBNB
                    element_click('//*[@id="back-to-top-anchor"]/div/div[2]/div[1]/div[3]/button[2]')
                    # opBNB CARV
                    element_click("//*[contains(text(),'CARV')]")
                    time.sleep(2)
                    # Metamask Confirm
                    web_jump_new()
                    confirm_path = '//*[@id="app-content"]/div/div/div/div[3]/div[3]/footer/button[2]'
                    while True:
                        try:
                            element_click(confirm_path)
                            break
                        except Exception:
                            time.sleep(0.5)
                else:
                    print(f"Account {wallet_number} Free Mint失败，即将进行下一个")
                    print()
            else:
                print(f"Account {wallet_number} Free Mint失败，按钮无法点击，即将进行下一个")
                print()
        wallet_number += 1

