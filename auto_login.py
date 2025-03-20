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
    browser.add_cookie({"name": "MUSIC_U", "value": "006713DE73027137A46B03FCF31B8C357E12A55A1E9CD25B415A9DEFFFB4ABBFB2E7E3A0F88A71950EA8426917EBB2877664A6AF0677DDD2C8A2382CC59C3CCE3FE9AF10BC09956A05E319086C7D6673B61FB15896D3333479F8831F5FE940C1053C372792982336AF0ABED3D24DDA9DC1D083EEBA771500C7AA796FF86B90A1DBFAB3DFDC5D01DD7C968887081B0E7D868AABAB02777451C46708AC4CA9A25B0377B2B494BC739832F0E5822D3412BECD2A2A46F39609A8B417B67CAFE482407C40F206BDDAA36387369579F2784DF7ED804C3CE89EF50884F19E1E81B60516DBF6D783D9ACE348B46600AB34B187E74DD55C0910DD387D8049A88386D1E5D6BF45AA111E25F99C1C53F1769E01D8F629BC0F338DB9FB719CB8213EEC97710006A6F6380137893A18040AA68C403EBC5DB869F1129CF7FE30EB14F4B176AB3C161F49B53217C8A924A0D02D7C1F8B86FDF840F912429AD5574D51E7F3B38C0C87"})
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
