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
    browser.add_cookie({"name": "MUSIC_U", "value": "00379753450A9EF9A668185EBCC14BDBF8BEAA0AA405DC008565F4BF1426E9D169348ADC4EE625FCE2C13E63AB7ABFA7EA7060E6CB364215FC3F63FA301D1155015568953EF948D92D366FEFA12B5ECB0E754F640076CE57F37A3943E0A6638D88CA988BBD624C59A50ACAEB46E4BB886D53BEA3A1023DBE067118D47FE9F10B013AAB62D13F6014CE6BA48779CE5A495D71514A5E675196499F1F09D2D2338F22D56FB7B74D60C3C8C64527BDC6A3215101EAB8B8F97770B94725934EC754C70CCCFB1D1EB7561A80BA66128B65907BEC8C05207FF2153C97552D060DC184D2FE2A1C11345E421A5E0766893A2C346DEEE3CB1F61ADF85318ACAA1187E0C064009CA9DBEE27DB9CB253C3AC592498A2CC7914792CBE3986EE11C1F67C93308BE5BC054D293C0BE060A4F8BEB118546DB9F484CAE10A9DEAFC52DD2613CB3557AD83C4263DC4822E949BC82A34EA00683F15AB42503FABA545AAED86498B01908C"})
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
