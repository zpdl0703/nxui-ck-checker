import os
import random
import time
from datetime import datetime
from pytz import timezone
from selenium.webdriver.common.by import By

import web_checker


def IsWeekend():
    d = datetime.now(timezone('Asia/Seoul'))
    if d.weekday() > 4:
        return True
    return False


def GetReport():
    if IsWeekend():
        return "오늘은 쉬었습니다."

    reportList = sorted(os.listdir("report_data"))

    result = ""

    for fileName in reportList:
        result += AppendReportStr("report_data/", fileName)

    return result


def AppendReportStr(path, fileName):
    file = open(path + fileName, "r", encoding='utf8')
    fileNameSplit = fileName.split(".")
    result = fileNameSplit[1] + "\n"
    strings = file.readlines()
    file.close()

    if fileNameSplit[2] == "sub":
        if random.randint(0, 10000) % 2 == 0:
            return ""

    result += random.choice(strings).strip().replace("\\n", "\n") + "\n\n"
    return result


if __name__ == '__main__':
    print("nxui ck checker")
    
    if IsWeekend():
        sys.exit(0)

    file = open("info.txt", "r", encoding='utf8')
    strings = file.readlines()
    file.close()

    url = strings[0]
    driver = web_checker.getDriver(url)

    print("==TRY LOGIN==")
    web_checker.login(driver, strings[1].strip(), strings[2].strip())
    driver.implicitly_wait(1)

    print("==GO TO MENU==")
    # 메뉴 이동
    web_checker.waitUntilFind(driver, (
        By.XPATH, "//div[@id='mainframe.WrapFrame.form.div_top.form.div_top.form.btn_siteMap']")).click()
    web_checker.waitUntilFind(driver, (By.XPATH,
                                       "//div[@id='mainframe.sitemap.form.div_wrap.form.Div_2842453_0.form.grd_menu"
                                       ".body.gridrow_0.cell_0_0:text']")).click()
    # 메뉴 유효성 확인
    web_checker.waitUntilFind(driver, (By.XPATH,
                                       "//div[@id='" + web_checker.nxuiHeader()
                                       + "form.div_work.form.div_detail.form.btn_save:icontext"
                                         "']"))
    driver.implicitly_wait(1)
    time.sleep(2)

    now = datetime.now(timezone('Asia/Seoul'))
    now_str = now.strftime("%m/%d")
    isWeekend = IsWeekend()

    print("==SELECT TODAY (1/2)==")
    # 캘린더 확인
    cal = driver.find_element(By.XPATH,
                              "//div[@id='" + web_checker.nxuiHeader()
                              + "form.div_work.form.grd_main.body']")
    driver.implicitly_wait(1)

    print("==SELECT TODAY (2/2)==")
    # 오늘 날짜 확인 및 클릭
    today = cal.find_element(By.XPATH, "//div[@aria-label='" + now_str + " ']")
    today.click()
    driver.implicitly_wait(1)

    print("==CHECK INFOS (1/4)==")
    # 출결상태
    web_checker.selectObjectNxui(driver,
                                 "//div[@id='" + web_checker.nxuiHeader()
                                 + "form.div_work.form.div_detail.form.cmb_atdabsCd']",
                                 "휴무" if isWeekend else "출석")
    print("==CHECK INFOS (2/4)==")
    # 실습 부서
    web_checker.insertFormNxui(driver, "//input[@id='" + web_checker.nxuiHeader()
                               + "form.div_work.form.div_detail.form.edt_pracDeptNm"
                                 ":input']", "딜펀"[::-1])
    print("==CHECK INFOS (3/4)==")
    # 실습 담당자
    userName = web_checker.getObject(driver, "//div[@id='" + web_checker.nxuiHeader()
                                     + "form.div_work.form.grd_info.body.gridrow_0.cell_0_5"
                                       ":text']")
    print("==CHECK INFOS (4/4)==")
    web_checker.insertFormNxui(driver, "//input[@id='" + web_checker.nxuiHeader()
                               + "form.div_work.form.div_detail.form.edt_pracTpicNm"
                                 ":input']", userName.text)

    print("==PRINTING==")
    # 실습 내용
    str_length = 0
    while str_length < 200:
        time.sleep(1)
        result_str = GetReport()
        print(result_str)
        web_checker.insertFormNxui(driver, "//textarea[@id='" + web_checker.nxuiHeader()
                                   + "form.div_work.form.div_detail.form.tar_pracCont"
                                     ":textarea']", result_str)
        time.sleep(1)
        str_length_str = web_checker.getObject(driver, "//div[@id='" + web_checker.nxuiHeader()
                                               + "form.div_work.form.div_detail.form.stt_cont"
                                                 ":text']").text
        str_length = int(''.join([i for i in str_length_str if i.isdigit()]))
        print("[총 " + str(str_length) + "자]")

    driver.implicitly_wait(1)
    print("==SAVING...==")
    # 저장
    web_checker.clickObject(driver, "//div[@id='" + web_checker.nxuiHeader()
                            + "form.div_work.form.div_detail.form.btn_save']")

    print("Result = " + web_checker.waitUntilFind(driver, (
        By.XPATH, "//div[contains(@id, '.form.btn_msg:icontext')]")).text)

    web_checker.waitUntilFind(driver, (
        By.XPATH, "//div[contains(@id, '.form.btn_yes:icontext')]")).click()

    print("==END==")
    time.sleep(2)

    web_checker.close(driver)
