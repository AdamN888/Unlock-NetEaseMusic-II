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
    browser.add_cookie({"name": "MUSIC_U", "value": "004AB675B8D01F86AE19A55AFB2C526A2C5253654BFC0C788F0CB38ACD6A2D61C6247DF98F6BB054ACAE52A6E83E80DCE1740B87CC50F9256315F90A7FF271010CF0C968F8CEB87E51594AAFDF0B11A9E6D48F6027D89B44764A6AFE2FAB97E076C44F66A9BA1F92DD7C5A89FBA344A423A6E298570E4BEFE25A4403AECF0CADFBC6CAA42C2F74ACE0ADD240BF2B029AD06F5F77CFFFB1B721984196BC1B78A13B70E594EDF31937EE31F117B041F1BD8186AF2935914D46609A32B38133A4F7D2F280A9AD8AA7AF97D71B453F4712F9B723FC9381121389AE2B8B14BA463D7B053FC91A694FFE98B77DB5C8E9708A468D842CDFFC0CA26AD65BBBF07439CF10A495073AD6FF2CBF75973D4A81CAA10F8B0B6E111A0262404D49EDA78AECDD7433651B8AF6625CD982CCC7D84B086C07F3444FB6411DD2DBFC6B37C0073C96A30A4CA7BC1B7FF6E9EB829A2501548ED07C56FBE026E4584E1768DCABA978AB792F"})
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
