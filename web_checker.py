from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
import time
import pyperclip


def getDriver(url):
    # 드라이버 로딩
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("lang=ko_KR")
    # TODO: 실제 사용 시 주석 해제 필요함
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("--no-sandbox")

    # chrome driver
    driver = webdriver.Chrome('chromedriver', chrome_options=options)
    driver.implicitly_wait(3)
    # driver.get(url)
    driver.maximize_window()

    time.sleep(2)

    return driver

def setUrl(driver, url):
    driver.get(url)
    time.sleep(2)

def clickObject(driver, obj_str):
    button = driver.find_element_by_css_selector(obj_str)
    button.click()

def selectObject(driver, obj_str, targetText):
    select = Select(driver.find_element_by_css_selector(obj_str))
    select.select_by_visible_text(targetText)

def login(driver, id, pw):
    driver.get("https://exp.ck.ac.kr/login.do")
    startLogin = driver.find_element_by_css_selector("div[class='loginField']")
    startLogin.find_element_by_css_selector("button[class='btnBasic btn_login']").click()
    driver.implicitly_wait(1)
    driver.find_element_by_css_selector("input[id='user_id']").send_keys(id)
    driver.implicitly_wait(1)
    driver.find_element_by_css_selector("input[id='user_pw']").send_keys(pw)
    driver.implicitly_wait(1)
    driver.find_element_by_css_selector("button[class='btnBasic btn_login w100']").click()

def insertForm(driver, obj_str, value):
    answer = driver.find_element_by_css_selector(obj_str)
    answer.send_keys(value)


def submit(driver):
    print("제출하기")
    submit_raw = driver.find_element_by_css_selector("button[menu='submitBtn']")
    driver.execute_script("arguments[0].scrollIntoView();", submit_raw)
    submit_raw.click()


def isSubmit(driver):
    return driver.find_element_by_class_name('finishMessage').get_attribute("textContent")

def acceptAlert(driver):
    try:
        alert = Alert(driver)
        alert.accept()
    except:
        print("No Alert!")


def close(driver):
    driver.close()
