import time
from telnetlib import EC
from selenium.webdriver import ActionChains
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from web3.middleware import geth_poa_middleware
from General.bit_api import *
import web3

from General.bit_api import openBrowser

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
    print(driver.title)
    return former_web


# 跳转至下一页面
def web_jump_next():
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])


# 跳转至指定页面
def web_jump_to(handle):
    driver.switch_to.window(handle)


def web_scroll(path):  # 滚动到某个元素的位置
    element = driver.find_element(By.XPATH, path)
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(2)


def web_scroll_top():  # 滚动到页面顶部
    js = 'window.scrollTo(0,0)'
    driver.execute_script(js)


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


def connect_all_wallet():
    # 如果已有账号登录
    if is_element_displayed('//*[@id="app"]/div/div[1]/header/div[2]/div/div/div[2]/div[2]/div/div[2]/p'):
        element_click('//*[@id="app"]/div/div[1]/header/div[2]/div/div/div[2]/div[2]/div/div[2]/p')
        # Disconnect
        element_click('/html/body/div[2]/div[3]/div/div/div/div[4]/div/p')
        # Login
        element_click('//*[@id="app"]/div/div[1]/header/div[2]/div/div/div[2]/div[2]/button')
        # Metamask
        element_click('/html/body/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[2]/div[1]/button')
    # 如果没有账号登录
    else:
        element_click('//*[@id="app"]/div/div[1]/header/div[2]/div/div/div[2]/div[2]/button')
        # Metamask
        element_click('/html/body/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[2]/div[1]/button')
    # 跳转至Metamask
    web_jump_new()
    is_element_displayed('//*[@id="app-content"]/div/div/div/div[2]/div[2]/div[1]/div[1]/input')
    # 全部选择
    element_click('//*[@id="app-content"]/div/div/div/div[2]/div[2]/div[1]/div[1]/input')
    time.sleep(3)
    # 下一步
    element_click('//*[@id="app-content"]/div/div/div/div[3]/div[2]/footer/button[2]')
    # 连接
    element_click('//*[@id="app-content"]/div/div/div/div[3]/div[2]/footer/button[2]')
    time.sleep(3)
    web_jump_new()
    # 签名
    element_click('//*[@id="app-content"]/div/div/div/div[4]/footer/button[2]')
    time.sleep(3)


def choose_wallet(number):
    action_chains = ActionChains(driver)
    # Account Button
    element_click('//*[@id="app-content"]/div/div[2]/div/button')
    # 滚动至第一个使用的账号位置
    path = "//*[contains(text(),'Account " + str(number) + "')]"
    # 点击切换账号
    is_element_displayed(path)
    element_click(path)
    # 账户选项
    element_click('//*[@id="app-content"]/div/div[2]/div/div[2]/div/div/button')
    # 账号详情
    element_click('//*[@id="popover-content"]/div[2]/button[1]')
    # 获取地址
    is_element_displayed('/html/body/div[3]/div[3]/div/section/div[2]/button')
    wallet_address = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/section/div[2]/div[2]/div['
                                                   '2]/div/div/button/span[1]/div').text
    # 显示私钥
    element_click('/html/body/div[3]/div[3]/div/section/div[2]/button')
    # 输入密码
    element_input('//*[@id="account-details-authenticate"]', 'Lkzxxzcsc2020')
    # 确认
    element_click('/html/body/div[3]/div[3]/div/section/div[5]/button[2]')
    # 长按以显示
    is_element_displayed('/html/body/div[3]/div[3]/div/section/div[2]/button')
    path = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/section/div[2]/button')
    action_chains.click_and_hold(path).perform()
    action_chains.release(path)
    # 获取私钥
    is_element_displayed('/html/body/div[3]/div[3]/div/section/div[3]/p')
    wallet_privateKey = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/section/div[3]/p').text
    wallet = {
        "address": wallet_address,
        "privateKey": wallet_privateKey
    }
    print(f'{wallet_address} 的私钥是 {wallet_privateKey}')
    return wallet


def login_address():
    # 如果已有账号登录
    if is_element_displayed('//*[@id="app"]/div/div[1]/header/div[2]/div/div/div[2]/div[2]/div/div[2]/p'):
        element_click('//*[@id="app"]/div/div[1]/header/div[2]/div/div/div[2]/div[2]/div/div[2]/p')
        # Disconnect
        element_click('/html/body/div[2]/div[3]/div/div/div/div[4]/div/p')
        # Login
        element_click('//*[@id="app"]/div/div[1]/header/div[2]/div/div/div[2]/div[2]/button')
        # Metamask
        element_click('/html/body/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[2]/div[1]/button')
    # 如果没有账号登录
    else:
        element_click('//*[@id="app"]/div/div[1]/header/div[2]/div/div/div[2]/div[2]/button')
        # Metamask
        element_click('/html/body/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[2]/div[1]/button')
    # 跳转至Metamask
    former_web = web_jump_new()
    # 签名
    is_element_displayed('//*[@id="app-content"]/div/div/div/div[4]/footer/button[2]')
    element_click('//*[@id="app-content"]/div/div/div/div[4]/footer/button[2]')
    print("账号已登录！")
    return former_web


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


def fetch_address():
    # 点击Free CARV
    is_element_displayed('//*[@id="back-to-top-anchor"]/div/div[3]/div[1]/div[2]/div[1]/div[1]/div/div[2]/button')
    element_click('//*[@id="back-to-top-anchor"]/div/div[3]/div[1]/div[2]/div[1]/div[1]/div/div[2]/button')
    # Top uo BNB
    element_click('/html/body/div[3]/div[3]/div/div[2]/div/div/div/div[1]/div[2]/div/div/button[2]')
    is_element_displayed('/html/body/div[4]/div[3]/div/div[2]/div[2]/div[2]/p')
    # 地址显示弹窗
    receive_address = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div/div[2]/div[2]/div[2]/p').text
    # 获取到收款地址
    print(f"收款地址：{receive_address}")
    return receive_address


def mint():
    while True:
        try:
            top_BNB_button = is_element_displayed('/html/body/div[4]/div[3]/div/div/div/button[2]')
            mint_button = is_element_displayed(
                '/html/body/div[3]/div[3]/div/div[2]/div/div/div/div[1]/div[2]/div/div/button')
            if top_BNB_button is False and mint_button is True:
                break
        except Exception as e:
            print(f'元素点击失败，请手动完成账号：{e}')
            return False


# 执行代码前确保主账号邀请链接正确
if __name__ == '__main__':
    # 初始化
    res = openBrowser('fb4694579e4048729d3ea86de12c7b8a')  # 比特浏览器窗口ID
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", res['data']['http'])
    service = Service(executable_path=res['data']['driver'])

    driver = webdriver.Chrome(service=service, options=chrome_options)
    # driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
    # # 导入所有钱包
    # import_private_key('100.1.json')

    # 进入邀请链接界面，手动连接所有钱包

    # 第一个钱包的编号
    wallet_number = 3
    last_wallet_number = 203
    # 共mint成功数量
    signed_number = 0
    while wallet_number <= last_wallet_number:
        # 小狐狸钱包切换账号
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
        wallet = choose_wallet(wallet_number)

        # 再次进入邀请链接界面
        driver.get('https://protocol.carv.io/airdrop?invite_code=AU7QF2')
        time.sleep(3)
        # 跳转至小狐狸
        former_web = web_jump_new()
        # 签名
        element_click('//*[@id="app-content"]/div/div/div/div[4]/footer/button[2]')

        time.sleep(3)
        driver.switch_to.window(former_web)
        driver.refresh()
        # 获取转账地址
        receive_address = fetch_address()

        # 转账至获取地址
        single_transfer(wallet['address'], wallet['privateKey'], receive_address)
        time.sleep(8)
        # 等待转账成功后，Mint按钮可以点击
        if mint() is not False:
            # 点击Mint
            element_click('/html/body/div[3]/div[3]/div/div[2]/div/div/div/div[1]/div[2]/div/div/button')
            time.sleep(8)
            # 跳转小狐狸
            web_jump_new()
            while True:
                if is_element_displayed('//*[@id="app-content"]/div/div/div/div[4]/footer/button[2]'):
                    break
            element_click('//*[@id="app-content"]/div/div/div/div[4]/footer/button[2]')
            # 等待Mint成功自动跳转
            time.sleep(10)
            # 成功后进行下一个账号
            signed_number += 1
            print(f"共有 {signed_number} 个账号Mint成功，即将进行下一个")
            print()
        wallet_number += 1










