# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00C79788953245E205461745862D69F4F9AC499495C4E422673F00D11F8E3423CA5C2BCF771F22E8EBBF02E4177C71BA28989A2577DDBBBE273552ED0DB3A87D5F49D4111DB4238927F1A010B8CA8F8032A1D682A5AAD5D333C755E703D663509A42B419BCC666C3333D8D85A5221BFAFA1BDAA611CBF940812650E7B805A7923FF6AD82532BAE43C08497FDF4F4DAA558F7AB3E417995D3CF68F9062122588F74C65671E842DE7D1E5DBA83C0296AD621ACF810029E4C9093DED61AE68E9F9709D2240650E6F68A92DB8519A0D5C411BF6F744FED320132D4F47973C29E6CE168D971A4ADBC99BF55545D78911853527B6A1D37E35504119A20139FEEC80DC9A89ECC6FF45170300F4388970CF39978619780DEF333F62B572883CBB90177FF69DD58ECE9049BCD1193B4F77C021D7BF67A452B014A6111653342735FA9EF4CF517ADE93636C8FA17BB7D0CD46E1F88F9585FD8D5036506DBD4441FDFF7625779"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
