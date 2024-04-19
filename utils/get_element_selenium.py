import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# Chrome Options
# https://peter.sh/experiments/chromium-command-line-switches/
# https://selenium-python.readthedocs.io/

root_folder = os.getcwd()
chrome_driver_path = os.path.join(root_folder, 'drivers', 'chromedriver')

def make_chrome_browser(*options: str) -> webdriver.Chrome:
    try:
        chrome_options = webdriver.ChromeOptions()

        # chrome_options.add_argument('--headless')
        if options is not None:
            for option in options:
                chrome_options.add_argument(option) # type: ignore

        chrome_service = Service(
            executable_path=str(chrome_driver_path),
        )

        browser = webdriver.Chrome(
            service=chrome_service,
            options=chrome_options,
        )
    except ExceptionGroup as e:
        print(f'Error: {e}')

    return browser

def get_element_data(url, xpath=None, link_text=None, partial_link_text=None, tag_name=None, class_name=None, css_selector=None):
    TIME_TO_WAIT = 10

    # Example
    # options = '--headless', '--disable-gpu'
    options = ()
    browser = make_chrome_browser(*options)

    browser.get(url)

    # Espere para encontrar o elemento
    if xpath:
        captured_element = browser.find_element(By.XPATH, xpath)
        #captured_element = WebDriverWait(browser, TIME_TO_WAIT).until(ec.visibility_of_element_located((By.XPATH, xpath)))
    elif link_text:
        captured_element = browser.find_element(By.LINK_TEXT, link_text)
    elif partial_link_text:
        captured_element = browser.find_element(By.PARTIAL_LINK_TEXT, partial_link_text)
    elif tag_name:
        captured_element = browser.find_element(By.TAG_NAME, tag_name)
    elif class_name:
        captured_element = browser.find_element(By.CLASS_NAME, class_name)
    elif css_selector:
        captured_element = browser.find_element(By.CSS_SELECTOR, css_selector)
    else:
        print(f'Elemento não identificado')

    print(f'\n\nElemento capturado: {captured_element.text}\n\n')

    captured_element.click()

    sleep(TIME_TO_WAIT)