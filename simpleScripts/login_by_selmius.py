import io

from PIL import Image
from selenium.webdriver import ActionChains

from baidu_Captcha_Ocr_res import orc_png_by_url, ocr_png_by_path
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Replace 'path_to_webdriver' with the actual path to the web driver executable
driver = webdriver.Chrome()

# Open the webpage
driver.get("http://172.20.251.8:31788/views/login.html")
username = "wyc"
password = "Wangyc0537@1"

time.sleep(3)
cance_bt_elem = driver.find_element(By.CSS_SELECTOR,
                                    "body > div.el-message-box__wrapper > div > div.el-message-box__btns > button:nth-child(1) > span")
cance_bt_elem.click()
time.sleep(2)

username_input = driver.find_element(By.XPATH, "/html/body/div/form/div[1]/div/div/input")
password_input = driver.find_element(By.XPATH, "/html/body/div/form/div[2]/div/div/input")
checkcode_img = driver.find_element(By.XPATH, "/html/body/div/form/div[3]/div/div[2]/img")
captcha_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='验证码']")

username_input.send_keys(username)
password_input.send_keys(password)
captcha_image_name = 'captcha.png'
max_attempts = 10
for attempts in range(max_attempts):
    try:
        if "index" in driver.current_url:
            print("登录成功")
            break
    except Exception as e:
        print("No")

    try:
        # 创建 ActionChains 对象
        actions = ActionChains(driver)

        # 将鼠标移动到目标元素
        actions.move_to_element(captcha_input).click_and_hold().perform()
        actions.click(checkcode_img).perform()
        time.sleep(5)
        # 位置
        location = checkcode_img.location
        size = checkcode_img.size
        # 使用 WebDriver 的截图功能，截取验证码图片
        captcha_image = driver.get_screenshot_as_png()
        captcha_image = Image.open(io.BytesIO(captcha_image))

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        captcha_image = captcha_image.crop((left, top, right, bottom))

        # 保存截取的验证码图片
        captcha_image.save(captcha_image_name)

        print("aa")
        time.sleep(5)
        # captcha_src = checkcode_img.get_attribute("src")
        # print(captcha_src)
        # data = orc_png_by_url(captcha_src)
        data = ocr_png_by_path(captcha_image_name)

        captcha_text = data.get('words_result')[0].get("words")
        if captcha_text == '' or captcha_text is None:
            # data = orc_png_by_url(captcha_src)
            data = ocr_png_by_path(captcha_image)
            captcha_text = data.get('words_result')[0].get("words")
        print(captcha_text)
        captcha_input.clear()
        time.sleep(2)
        captcha_input.send_keys(captcha_text)
        err_elem = driver.find_element(By.XPATH, "/html/body/div[1]/form/div[3]/div/div[3]")
        print(err_elem.text)
        submit_button = driver.find_element(By.XPATH, "/html/body/div/form/div[4]/div/button")
        submit_button.click()
        time.sleep(1)
    except Exception as e:
        print(e)

        # captcha_input.clear()
        time.sleep(1)

        # continue

# Wait for a few seconds to see the result
time.sleep(5)

# Submit the form (if there's a submit button)


time.sleep(10)
# Close the browser
driver.quit()
