from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

from typing import Optional, List,Tuple
import time
import random
import platform
import sys
import os

#生成资源文件目录访问路径
def resource_path(relative_path):
    if getattr(sys, 'frozen', False): #是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Question:
    def __init__(self, question:WebElement, options: Optional[list[WebElement]] = None) -> None:
        self.__question = question
        self.__options = options

    def click(self, index:int):
        if self.__options is not None and isinstance(self.__options, List):
            self.__options[index].click()
        else:
            print("注意接口查找错误")

    #//a[@class="rate-off rate-offlarge"]
    def get_options(self) -> List[str]:
        if self.__options is None:
            return []
        return [x.get_attribute('title') for x in self.__options]

    #//div[@class="field-label"]
    def get_question(self) -> str:
        return self.__question.text

class Submit:
    def __init__(self, driver:WebDriver) -> None:
        self.__diver = driver

    def click(self):
        if isinstance(self.__diver, WebDriver):
            self.__diver.find_element(By.ID, 'ctlNext').click()
            time.sleep(0.5)
            try:
                comfirmdel = self.__diver.find_element(
                    By.XPATH, '//a[@class="layui-layer-btn0"]')
                comfirmdel.click()
                time.sleep(0.5)
                validation = self.__diver.find_element(By.XPATH, '//div[@id="rectMask"]')
                validation.click()
                time.sleep(4)
            except:
                pass
        else:
            raise TypeError


class Wenjuan:
    def __init__(self) -> None:
        if platform.system() == 'Windows':
            options = webdriver.EdgeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--headless')
            self.driver = webdriver.Edge(options=options)
        else:
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            # chrome 88 或更高版本的反爬虫特征处理
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--headless')
            self.driver = webdriver.Chrome(options=options)
        with open(resource_path('stealth.min.js')) as stealth:
            stealthjs = stealth.read()
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": stealthjs
            })

    def __del__(self):
        self.driver.quit()

    def reload(self, url: str):
        self.driver.get(url)
        self.driver.execute_script(
            "var q=document.documentElement.scrollTop=0")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'ctlNext')))

    def fetch_questions(self, url: str) -> Tuple[List[Question], Submit]:
        elements = []
        self.reload(url)
        questions = self.driver.find_elements(By.XPATH, '//div[@class="field-label"]')
        for (i, title) in enumerate(questions):
            # 获取每个问题的
            answers = self.driver.find_elements(By.XPATH, f'//div[@id="div{i+1}"]//a[@class="rate-off rate-offlarge"]')
            elements.append(Question(title, answers if len(answers) != 0 else None))
        return (elements, Submit(self.driver))


if __name__ == '__main__':
    wenjuan = Wenjuan()
    # wenjuan.answer_question('https://www.wjx.cn/vm/tibXV8t.aspx')
    wenjuan.fetch_questions('https://www.wjx.cn/vm/tibXV8t.aspx')
    (questions, submit) = wenjuan.fetch_questions('https://www.wjx.cn/vm/tibXV8t.aspx')

    for question in questions:
        print(question.get_question())
        print(question.get_options())
        options = len(question.get_options())
        if options > 0 :
            index = random.randint(0, len(question.get_options())-1)
            print(index)
            question.click(index)

    submit.click()
    time.sleep(4)