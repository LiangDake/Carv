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


def is_element_displayed_in_1s(path):
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
            element_click('/html/body/div[3]/div[3]/div/section/div[5]/button')
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


if __name__ == '__main__':
    # 设置Chrome选项
    chrome_options = Options()
    # 添加Ronin插件
    chrome_options.add_experimental_option('detach', True)
    chrome_options.add_extension(
        '/Users/liangdake/Downloads/工作/Ronin-Wallet.crx')  # 将"path_to_extension.crx"替换为插件文件的路径
    # 指定用户数据目录，以便保存缓存等数据
    chrome_options.add_argument('--user-data-dir=/Users/liangdake/Downloads/工作/data')
    # 启动Chrome浏览器
    driver = webdriver.Chrome(options=chrome_options)

    # # 导入所有MetaMask钱包
    # driver.get('chrome-extension://giljdnlnedpfminddbaiffifgnjcpcof/home.html')
    # if is_element_displayed('//*[@id="password"]'):
    #     element_input('//*[@id="password"]', 'Lkzxxzcsc2020')
    #     element_click('//*[@id="app-content"]/div/div[2]/div/div/button')
    # import_private_key('/Users/liangdake/PycharmProjects/Carv/Wallets/100.1.json')

    # # 导入所有Ronin钱包
    # # 进入ronin wallet界面
    # driver.get('chrome-extension://fnjhmkhhmkbjkkabndcnnogagogbneec/popup.html#/')
    # if is_element_displayed('//*[@id="password-input"]'):
    #     element_input('//*[@id="password-input"]', 'Lkzxxzcsc2020')
    #     element_click('//*[@id="root"]/div[1]/div/form/div/button')
    #     # 点击头像
    #     element_click('//*[@id="root"]/div[1]/div/div/div[1]/div[1]/button')
    # for i in range(1, 103):
    #     # 点击Create Wallet
    #     element_click('//*[@id="root"]/div[1]/div/div[4]/div[1]/div[1]/div[2]/div[1]')
    #     # Create
    #     element_click('/html/body/div[5]/div[2]/div/div/div[2]/button[2]')
    #
    # 导入完成钱包后手动进行钱包绑定

    # 开始运行
    # 第一个钱包的编号
    wallet_number = 96
    last_wallet_number = 106
    while wallet_number <= last_wallet_number:
        driver.get('chrome-extension://giljdnlnedpfminddbaiffifgnjcpcof/home.html')
        # 小狐狸钱包切换账号
        # 登录页面
        if is_element_displayed_in_1s('//*[@id="password"]'):
            element_input('//*[@id="password"]', 'Lkzxxzcsc2020')
            element_click('//*[@id="app-content"]/div/div[2]/div/div/button')
        # 切换账号
        choose_wallet(wallet_number)
        time.sleep(1)
        # 进入ronin wallet切换账号
        driver.get('chrome-extension://fnjhmkhhmkbjkkabndcnnogagogbneec/popup.html#/')
        if is_element_displayed_in_1s('//*[@id="password-input"]'):
            element_input('//*[@id="password-input"]', 'Lkzxxzcsc2020')
            element_click('//*[@id="root"]/div[1]/div/form/div/button')
        if is_element_displayed_in_1s('/html/body/div[4]/div[2]/div/div/button[1]'):
            element_click('/html/body/div[4]/div[2]/div/div/button[1]')
        # 点击人头像
        element_click('//*[@id="root"]/div[1]/div/div/div[1]/div[1]/button')
        # 选择钱包
        path = "//*[contains(text(),'Account #" + str(wallet_number) + "')]"
        element_click(path)
        time.sleep(1)
        # 进入Carv界面
        driver.get('https://protocol.carv.io/airdrop?invite_code=AU7QF2')
        if is_element_displayed_in_1s('//*[@id="app"]/div/div[1]/header/div[2]/div/div/div[2]/div[2]/button'):
            element_click('//*[@id="app"]/div/div[1]/header/div[2]/div/div/div[2]/div[2]/button')
            time.sleep(0.5)
            element_click('/html/body/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[2]/div[1]/button/div/div/div[2]/div')
        # 跳转至小狐狸
        former_web = web_jump_new()
        # 签名
        element_click("//*[contains(text(),'签名')]")
        web_jump_to(former_web)
        driver.switch_to.window(former_web)
        driver.refresh()
        # 再次跳转签名页面
        former_web = web_jump_new()
        # 签名
        element_click('//*[@id="app-content"]/div/div/div/div[4]/footer/button[2]')
        time.sleep(1)
        element_click('//*[@id="app-content"]/div/div/div/div[4]/footer/button[2]')
        web_jump_to(former_web)
        time.sleep(2)
        # Ronin SOUL Bind
        ronin_path = '//*[@id="back-to-top-anchor"]/div/div[3]/div[1]/div[2]/div/div[1]/div/div[4]/div/div[2]/div[2]/button'
        element_click(ronin_path)
        if is_element_displayed_in_1s('/html/body/div[3]/div[3]/div/div[2]/div/div/div/div[1]/div[2]/div/div/button[2]'):
            print(f"Account {wallet_number} 未注册，即将进行下一个")
            print()
        else:
            # 跳转至Ronin
            former_web = web_jump_new()
            # Sign是否出现
            element_click('//*[@id="root"]/div[1]/div/div[2]/div/div[2]/div[2]/div/button[2]')
            time.sleep(2)
            web_jump_to(former_web)
            # Free CARV
            carv_path = "//*[contains(text(),'Free CARV')]"
            element_click(carv_path)
            time.sleep(2)
            # 成功后进行下一个账号
            print(f"Account {wallet_number} Ronin钱包绑定成功，即将进行下一个")
            print()
        wallet_number += 1
