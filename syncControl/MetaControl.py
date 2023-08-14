import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import typing
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
import re

url = "http://172.20.251.8:31788/views/login.html"
remote_url = "127.0.0.1:9222"
filename = "createMeta.json"


def get_handle(titlename: str, browser, handles):
    for handle in handles:
        browser.switch_to.window(handle)
        if titlename in browser.title:
            return handle


def res_data(f: str):
    with open(f, 'r', encoding="utf-8") as f:
        data = json.load(f)
    return data


# 创建网元
def create_meta(browser: webdriver, data: dict):
    # 进入form，
    # areaname
    areaNameElement = browser.find_element(By.XPATH,
                                           "/html/body/div[1]/div[3]/div/div[2]/form/div/div[1]/div/div/div[1]/div[1]/div[2]/input")
    browser.implicitly_wait(1)
    ac_areaname_element = ActionChains(browser)
    areaName = data.get('area')
    ac_areaname_element.move_to_element(areaNameElement).perform()
    areaNameElement.send_keys(areaName)
    area_pod_elem = browser.find_element(By.CSS_SELECTOR,
                                         "body > div.app-container > div:nth-child(4) > div > div.el-dialog__body > form > div > div:nth-child(1) > div > div > div.vue-treeselect__menu-container")
    items = area_pod_elem.find_elements(By.CLASS_NAME, 'vue-treeselect__label-container')
    for item in items:
        try:
            if item.text == areaName:
                print("-----")
                ActionChains(browser).click(item).perform()
        except Exception as e:
            continue
    # 数据
    egionDesc = data.get("egionDesc")
    devname = data.get("devname", "1")
    devIP = data.get("devIP")
    vendorname = data.get("vendorname")
    devtypeDesc = data.get("devtypeDesc")
    devtype = data.get("devtype")
    OSVersion = data.get("OSVersion")
    egion = data.get("egion")
    devstype = data.get("devstype")

    # 网元名称
    browser.find_element(By.XPATH,
                         "/html/body/div[1]/div[3]/div/div[2]/form/div/div[2]/div/div/input").send_keys(devname)
    # 管理IP
    browser.find_element(By.XPATH,
                         "/html/body/div[1]/div[3]/div/div[2]/form/div/div[3]/div/div/input").send_keys(devIP)
    # 专业
    browser.find_element(By.XPATH,
                         "/html/body/div[1]/div[3]/div/div[2]/form/div/div[5]/div/div/div/input").send_keys(devstype)
    items = browser.find_elements(By.CLASS_NAME, "el-select-dropdown__item")
    for item in items:
        try:
            if item.text == devstype:
                ActionChains(browser).click(item).perform()
        except Exception as e:
            continue
    # 厂家
    browser.find_element(By.XPATH,
                         "/html/body/div[1]/div[3]/div/div[2]/form/div/div[6]/div/div/div/input").send_keys(vendorname)
    items = browser.find_elements(By.CLASS_NAME, "el-select-dropdown__item")
    for item in items:
        try:
            if item.text == vendorname:
                ActionChains(browser).click(item).perform()
        except Exception as e:
            continue

    # 网元系类
    browser.find_element(By.XPATH,
                         "/html/body/div[1]/div[3]/div/div[2]/form/div/div[8]/div/div/div/input").send_keys(devtypeDesc)
    browser.implicitly_wait(5)
    all_ul_eles = browser.find_element(By.CSS_SELECTOR,
                                       "body > div:nth-child(18) > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul")
    items = all_ul_eles.find_elements(By.TAG_NAME, "li")
    for item in items:

        try:
            span_text = item.find_element(By.TAG_NAME, 'span')
            print(span_text.text)
            if devtypeDesc in span_text.text and egionDesc in span_text.text:
                print(span_text.text)
                ActionChains(browser).click(item).perform()
        except Exception as e:
            continue

    # 网元型号
    browser.find_element(By.XPATH,
                         "/html/body/div[1]/div[3]/div/div[2]/form/div/div[9]/div/div/div/input").send_keys(devtype)
    items = browser.find_elements(By.CLASS_NAME, "el-select-dropdown__item")
    for item in items:
        try:
            if devtype in item.text:
                ActionChains(browser).click(item).perform()
        except Exception as e:
            continue
    # 网元域
    browser.find_element(By.XPATH,
                         "/html/body/div[1]/div[3]/div/div[2]/form/div/div[10]/div/div[1]/div/input").send_keys(egion)
    items = browser.find_elements(By.CLASS_NAME, "el-select-dropdown__item")
    for item in items:
        try:
            if egion == item.text:
                ActionChains(browser).click(item).perform()
        except Exception as e:
            continue
    # OS版本
    browser.find_element(By.XPATH,
                         "/html/body/div[1]/div[3]/div/div[2]/form/div/div[11]/div/div/div/input").send_keys(OSVersion)
    items = browser.find_elements(By.CLASS_NAME, "el-select-dropdown__item")
    for item in items:
        try:
            if OSVersion == item.text:
                ActionChains(browser).click(item).perform()
        except Exception as e:
            continue

    # 网元类型
    browser.find_element(By.XPATH,
                         "/html/body/div[1]/div[3]/div/div[2]/form/div/div[7]/div/div/div/input").send_keys(egionDesc)
    items = browser.find_elements(By.CLASS_NAME, "el-select-dropdown__item")
    for item in items:
        try:
            if egionDesc in item.text and egion in item.text:
                ActionChains(browser).click(item).perform()
        except Exception as e:
            continue

    # 取消
    browser.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div[3]/div/button[1]").click()

    # 确认
    # browser.find_element(By.XPATH,"/html/body/div[1]/div[3]/div/div[3]/div/button[2]").click()

# 采控源
def select_control_meta(browser:webdriver,data:dict):
    egionDesc = data.get("egionDesc")
    devname = data.get("devname", "1")
    devIP = data.get("devIP")
    vendorname = data.get("vendorname")
    devtypeDesc = data.get("devtypeDesc")
    devtype = data.get("devtype")
    OSVersion = data.get("OSVersion")
    egion = data.get("egion")
    devstype = data.get("devstype")
    area = data.get("area")
    # 选专业
    temp_elem = browser.find_element(By.XPATH,"/html/body/div[1]/div[3]/div/div[2]/form/div[1]/div/div/div/div/input")
    browser.implicitly_wait(3)
    ActionChains(browser).move_to_element(temp_elem).perform()
    ActionChains(browser).click(temp_elem).perform()
    browser.implicitly_wait(3)
    temp_elem1 = browser.find_element(By.CSS_SELECTOR,"body > div.el-select-dropdown.el-popper > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul > li.el-select-dropdown__item.selected") #/html/body/div[3]/div[1]/div[1]/ul/li[4]
    browser.implicitly_wait(3)
    ActionChains(browser).move_to_element(temp_elem1).perform()
    browser.implicitly_wait(3)
    ActionChains(browser).click(temp_elem1).perform()
    # 选模板
    browser.find_element(By.XPATH,"/html/body/div[1]/div[3]/div/div[2]/form/div[2]/button").click()
    browser.implicitly_wait(1)
    browser.find_element(By.XPATH,"/html/body/div[1]/div[4]/div/div[2]/form/div[1]/div[2]/div/div/input").send_keys(area)
    browser.find_element(By.XPATH,"/html/body/div[1]/div[4]/div/div[2]/form/div[2]/div/div/button").click()
    browser.implicitly_wait(5)
    # 查询模板
    tbody_elem = browser.find_element(By.XPATH,"/html/body/div[1]/div[4]/div/div[2]/div[1]/div[3]/table/tbody")
    trs_elems = tbody_elem.find_element(By.TAG_NAME,"tr")
    print(trs_elems[0])
    text = trs_elems[1].find_element(By.TAG_NAME,"div").text
    print(text)


def startMeta():
    # 控制浏览器
    options = Options()
    options.add_experimental_option("debuggerAddress", remote_url)
    browser = webdriver.Chrome(options=options)
    handles = browser.window_handles
    handle = get_handle('新一代', browser, handles)
    browser.switch_to.window(handle)

    # # 左侧选中想要的菜单；网元管理
    # clickable = browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/ul/li[4]/span")
    # ActionChains(browser).move_to_element(clickable).perform()
    # browser.implicitly_wait(1)
    # browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/ul[6]/li").click()
    #
    # # 切换到右边然后新增；
    # browser.switch_to.frame(browser.find_element(By.XPATH, "//iframe[contains(@src,'device')]"))
    # browser.implicitly_wait(1)
    # # 点击新增，打开网元创建
    # browser.find_element(By.XPATH, "//button[span[text()='新增']]").click()
    #
    # # 网元创建
    data = res_data(filename).get("datas")[0]
    # # create_meta(browser, data)
    #
    # browser.switch_to.parent_frame()
    # 左侧选中想要的菜单；采控源管理
    clickable = browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/ul/li[4]/span")
    ActionChains(browser).move_to_element(clickable).perform()
    browser.implicitly_wait(1)
    browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/ul[7]/li").click()

    # 切换到右边然后新增；
    browser.switch_to.frame(browser.find_element(By.XPATH, "//iframe[contains(@src,'resource')]"))
    browser.implicitly_wait(1)
    # 点击新增，打开网元创建
    browser.find_element(By.XPATH, "//button[span[text()='新增']]").click()

    select_control_meta(browser,data)


if __name__ == '__main__':
    startMeta()
