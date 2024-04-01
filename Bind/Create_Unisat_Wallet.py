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


# 执行代码前确保主账号邀请链接正确
if __name__ == '__main__':
    # 初始化
    res = openBrowser('b67b48b12c94480ab8d54ecbc692e722')  # 比特浏览器窗口ID
    chrome_options = Options()
    chrome_options.add_argument("headless")  ##无头模式
    chrome_options.add_experimental_option("debuggerAddress", res['data']['http'])
    service = Service(executable_path=res['data']['driver'])
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # 进入unisat界面
    driver.get('chrome-extension://ppbibelpcjmhbdihakflkdcoccbgbkpo/index.html#/main')
    # 第一个钱包的编号
    wallet_number = 2
    last_wallet_number = 102
    while wallet_number <= last_wallet_number:
        if is_element_displayed('//*[@id="root"]/div[1]/div/div[2]/div/div[1]'):
            element_click('//*[@id="root"]/div[1]/div/div[2]/div/div[1]')
            # Add Account
            path = '//*[@id="root"]/div[1]/div/div[1]/div/div[3]/div'
            print(is_element_displayed(path))
            element_click(path)
            # Create an Account
            element_click('//*[@id="root"]/div[1]/div/div[2]/div/div[2]')
            print(f"第 {wallet_number} 个钱包创建成功")
            wallet_number += 1
            time.sleep(2)

