import os
import random
import time
from datetime import datetime
from pytz import timezone

import web_checker


def IsWeekend():
    d = datetime.now(timezone('Asia/Seoul'))
    if d.weekday() > 4:
        return True
    return False

def GetReport():

    if IsWeekend():
        return "오늘은 쉬었습니다."

    reportList = os.listdir("report_data")

    result = ""

    for fileName in reportList:
        result += AppendReportStr("report_data/", fileName)

    return result

def AppendReportStr(path, fileName):
    file = open(path + fileName, "r", encoding='utf8')
    fileNameSplit = fileName.split(".")
    result = "[" + fileNameSplit[1] + "]\n"
    strings = file.readlines()
    file.close()

    if fileNameSplit[2] == "sub":
        if random.randint(0, 10000) % 2 == 0:
            return ""

    result += random.choice(strings).strip().replace("\\n", "\n") + "\n\n"
    return result

if __name__ == '__main__':
    print("exp ck checker")

    file = open("info.txt", "r", encoding='utf8')
    strings = file.readlines()
    file.close()

    url = strings[0]
    driver = web_checker.getDriver(url)

    web_checker.login(driver, strings[1].strip(), strings[2].strip())
    time.sleep(2)
    web_checker.setUrl(driver, strings[0].strip())

    now = datetime.now(timezone('Asia/Seoul'))
    now_str = now.strftime("%Y%m%d")
    isWeekend = IsWeekend()

    driver.implicitly_wait(1)
    time.sleep(2)
    web_checker.clickObject(driver, "td[id='" + now_str + "']")
    time.sleep(1)
    web_checker.selectObject(driver, "select[id='pims_stat']", "휴무" if isWeekend else "출석")
    time.sleep(1)
    web_checker.insertForm(driver, "textarea[id='tody_rslt']", GetReport())
    time.sleep(1)
    web_checker.clickObject(driver, "button[id='btnSave']")
    time.sleep(1)
    web_checker.acceptAlert(driver)
    time.sleep(1)
    web_checker.acceptAlert(driver)

    time.sleep(3)

    web_checker.close(driver)


