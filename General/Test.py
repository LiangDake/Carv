import csv
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
from bit_api import *
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


# 执行代码前确保主账号邀请链接正确
if __name__ == '__main__':
    # 初始化
    res = openBrowser('c64174a092c64d0aa02459916a96783f')  # 比特浏览器窗口ID
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", res['data']['http'])
    service = Service(executable_path=res['data']['driver'])

    driver = webdriver.Chrome(service=service, options=chrome_options)
    # driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
    # # 导入所有钱包
    # import_private_key('2024-1-14_mnemonic_address_bot.json')

    # 进入邀请链接界面，手动连接所有钱包

    # 第一个钱包的编号
    wallet_number = 3
    last_wallet_number = 203
    while wallet_number <= last_wallet_number:
        # 小狐狸钱包切换账号
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
        wallet = choose_wallet(wallet_number)
        # 再次进入邀请链接界面
        driver.get('https://protocol.carv.io/airdrop?invite_code=AU7QF2')
        # 跳转至小狐狸
        former_web = web_jump_new()
        # 签名
        element_click('//*[@id="app-content"]/div/div/div/div[4]/footer/button[2]')
        time.sleep(2)
        driver.switch_to.window(former_web)
        driver.refresh()

        # 可能会再次需要签名
        attempt = 5
        new_window_handle = None
        former_web = driver.current_window_handle
        while not new_window_handle and attempt > 0:
            for handle in driver.window_handles:
                if handle != former_web:
                    new_window_handle = handle
            attempt -= 1
            time.sleep(1)
        if new_window_handle is not None:
            driver.switch_to.window(new_window_handle)
            # 签名
            element_click('//*[@id="app-content"]/div/div/div/div[4]/footer/button[2]')
            time.sleep(2)
            driver.switch_to.window(former_web)

        # Free Mint
        if is_element_displayed('//*[@id=":r5:"]'):
            element_click('//*[@id=":r5:"]')
            time.sleep(1)
            if is_element_displayed('/html/body/div[3]/div[3]/div/div[2]/div/div[2]/button'):
                element_click('/html/body/div[3]/div[3]/div/div[2]/div/div[2]/button')
                # 成功后进行下一个账号
                print(f"Account {wallet_number} Free Mint成功，即将进行下一个")
                print()
            else:
                print(f"Account {wallet_number} Free Mint失败，即将进行下一个")
                print()
        else:
            print(f"Account {wallet_number} Free Mint失败，按钮无法点击，即将进行下一个")
            print()
        # 准备进行下一个钱包
        wallet_number += 1

