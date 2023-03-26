from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import random
import threading
import pdb

class Wenjuan:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chrome 88 或更高版本的反爬虫特征处理
        options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome()
        with open('stealth.min.js') as stealth:
            stealthjs = stealth.read()
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": stealthjs
            })

    def __del__(self):
        self.driver.quit()

    def answer_question(self, url: str):
        self.driver.get(url)
        self.driver.execute_script(
            "var q=document.documentElement.scrollTop=0")
        time.sleep(2)
        WebDriverWait(self.driver, 1000).until(
            EC.presence_of_element_located((By.ID, 'ctlNext'))
        )

        total = 100
        # 1、获取题目，遍历
        titles = self.driver.find_elements(
            By.XPATH, '//div[@class="field-label"]')
        for (i, title) in enumerate(titles):
            # 获取每个问题的
            print(title.text)
            answers = self.driver.find_elements(
                By.XPATH, f'//div[@id="div{i+1}"]//a[@class="rate-off rate-offlarge"]')
            print([x.get_attribute('title') for x in answers])
            if len(answers) == 0:
                continue
           
            check = 0 if random.random() < 0.8 else 1
            total -= check
            if total <= 98:
                check = 0
            answers[check].click()
            time.sleep(0.2)
        # 点击提交
        self.driver.find_element(By.ID, 'ctlNext').click()
        time.sleep(0.5)

        try:
            comfirmdel = self.driver.find_element(
                By.XPATH, '//a[@class="layui-layer-btn0"]')
            comfirmdel.click()
            time.sleep(0.5)
            validation = self.driver.find_element(By.XPATH, '//div[@id="rectMask"]')
            validation.click()
        except:
            pass
        
        time.sleep(4)
        print(f'已填写完问卷')

if __name__ == '__main__':
    wenjuan = Wenjuan()
    wenjuan.answer_question('https://www.wjx.cn/vm/tibXV8t.aspx')
