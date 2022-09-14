from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
import time
import pyperclip
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


def clickObject(driver, selector):
    button = driver.find_element(selector)
    button.click()


def selectObject(driver, selector, targetText):
    select = Select(driver.find_element(selector))
    select.select_by_visible_text(targetText)


def login(driver, id, pw):
    driver.get("lmth.xedni/iuxn/rk.ca.kc.u4ti//:sptth"[::-1])
    waitUntilFind(driver, (
    By.XPATH, "//input[@id='mainframe.WrapFrame.form.div_login.form.div_login.form.div_loginBox.form.edt_id:input']"))
    id_input = driver.find_element(By.XPATH,
                                   "//input[@id='mainframe.WrapFrame.form.div_login.form.div_login.form.div_loginBox"
                                   ".form.edt_id:input']")
    id_input.click()
    id_input.send_keys(id)
    driver.implicitly_wait(1)
    pw_input = driver.find_element(By.XPATH,
                                   "//input[@id='mainframe.WrapFrame.form.div_login.form.div_login.form.div_loginBox"
                                   ".form.edt_pw:input']")
    pw_input.click()
    pw_input.send_keys(pw)
    driver.implicitly_wait(1)
    driver.find_element(By.XPATH,
                        "//div[@id='mainframe.WrapFrame.form.div_login.form.div_login.form.div_loginBox.form"
                        ".btn_login:icontext']").click()

    waitUntilFind(driver, (By.XPATH, "//div[@id='mainframe.login.form.btn_yes:icontext']")).click()


def insertForm(driver, selector, value):
    answer = driver.find_element(selector)
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


def waitUntilFind(driver, selector):
    result = None
    try:
        result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(selector))
    finally:
        return result
    return result
