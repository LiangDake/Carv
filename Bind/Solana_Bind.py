import csv
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


# 执行代码前确保主账号邀请链接正确
if __name__ == '__main__':
    # 初始化
    res = openBrowser('bb9a5b3c33f14fcca2e96ac144c532d8')  # 比特浏览器窗口ID
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", res['data']['http'])
    service = Service(executable_path=res['data']['driver'])

    # 第一个钱包的编号
    wallet_number = 76
    last_wallet_number = 106
    while wallet_number <= last_wallet_number:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
        # 小狐狸钱包切换账号
        choose_wallet(wallet_number)
        # 进入unisat界面
        driver.get('chrome-extension://bfnaelmomeimhlpmgjnjophhpkkoljpa/popup.html')
        # 菜单栏
        element_click('//*[@id="root"]/div/section/div[1]/div')
        # 添加钱包
        element_click('//*[@id="root"]/div/div[6]/div/div[3]/div[1]/div/div')
        time.sleep(1)
        # Create New Account
        element_click('//*[@id="root"]/div/div[6]/div/div/div/div[1]')
        # Create
        element_click('//*[@id="root"]/div/div[6]/div/div/form/div/div[2]/button[2]')
        time.sleep(2)
        # 进入Carv界面
        driver.get('https://protocol.carv.io/airdrop?invite_code=AU7QF2')
        # 跳转至小狐狸
        former_web = web_jump_new()
        # 签名
        element_click('//*[@id="app-content"]/div/div/div/div[4]/footer/button[2]')
        time.sleep(2)
        driver.switch_to.window(former_web)
        driver.refresh()
        time.sleep(2)
        # 移动页面
        path = "//*[contains(text(),'Mining Speed')]"
        web_scroll(path)
        element_click('//*[@id="back-to-top-anchor"]/div/div[3]/div[1]/div[2]/div/div[3]/div/div')
        time.sleep(1)
        # Solana SOUL Bind
        solana_path = '//*[@id="back-to-top-anchor"]/div/div[3]/div[1]/div[2]/div/div[1]/div/div[6]/div/div[2]/div[2]/button'
        element_click(solana_path)
        if is_element_displayed_in_2s('/html/body/div[3]/div[3]/div/div[2]/div/div/div/div[1]/div[2]/div/div/button[2]'):
            print("此账号未注册，即将进行下一个")
        else:
            # 跳转至Bitcoin
            former_web = web_jump_new()
            # Connect是否出现
            if is_element_displayed('//*[@id="root"]/div/div[1]/div[2]/div/button[2]'):
                # Connect
                element_click('//*[@id="root"]/div/div[1]/div[2]/div/button[2]')
                web_jump_to(former_web)
                # 跳转签名页面
                former_web = web_jump_new()
                # Sign In
                if is_element_displayed('//*[@id="root"]/div/div[1]/div/div[2]/div/button[2]'):
                    element_click('//*[@id="root"]/div/div[1]/div/div[2]/div/button[2]')
                web_jump_to(former_web)
                # # 移动页面
                # path = "//*[contains(text(),'Transaction History')]"
                # web_scroll(path)
                # # Free CARV
                # carv_path = "//*[contains(text(),'Free CARV')]"
                # element_click(carv_path)
                # time.sleep(1)
                # # 成功后进行下一个账号
                # print(f"Account {wallet_number} Solana钱包绑定成功，即将进行下一个")
                # print()

                time.sleep(3)
                # 移动页面
                path = "//*[contains(text(),'Transaction History')]"
                web_scroll(path)
                time.sleep(1)
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
                        print(f"Account {wallet_number} opBNB Mint成功，即将进行下一个")
                        time.sleep(2)
                        break
                    except Exception:
                        time.sleep(0.5)


        wallet_number += 1

