from pathlib import Path
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

ROOT_FOLDER = Path.cwd()
CHROME_DRIVER_PATH = ROOT_FOLDER / 'drivers' / 'chromedriver'

def make_chrome_browser(*options: str) -> webdriver.Chrome:
    try:
        chrome_options = webdriver.ChromeOptions()

        # chrome_options.add_argument('--headless')
        if options is not None:
            for option in options:
                chrome_option.add_argument(option) # type: ignore

        chrome_service = Service(
            executable_path=str(CHROME_DRIVER_PATH),
        )

        browser = webdriver.Chrome(
            service=chrome_service,
            options=chrome_options,
        )
    except ExceptionGroup as e:
        print(f'Error: {e}')

    return browser

def get_element_data(url, time, xpath=None, link_text=None, partial_link_text=None, tag_name=None, class_name=None, css_selector=None):
    TIME_TO_WAIT = time

    # Example
    # options = '--headless', '--disable-gpu'
    options = ()
    browser = make_chrome_browser(*options)

    browser.get(url)

    # Espere para encontrar o input
    try:
        if xpath:
            captured_element = WebDriverWait(browser, TIME_TO_WAIT).until(ec.presence_of_element_located((By.XPATH, xpath)))
            return captured_element
        elif link_text:
            WebDriverWait(browser, TIME_TO_WAIT).until(ec.presence_of_element_located((By.LINK_TEXT, link_text)))
            return 
        elif partial_link_text:
            captured_element = WebDriverWait(browser, TIME_TO_WAIT).until(ec.presence_of_element_located((By.PARTIAL_LINK_TEXT, partial_link_text)))
            return captured_element
        elif tag_name:
            captured_element = WebDriverWait(browser, TIME_TO_WAIT).until(ec.presence_of_element_located((By.TAG_NAME, tag_name)))
            return captured_element
        elif class_name:
            captured_element = WebDriverWait(browser, TIME_TO_WAIT).until(ec.presence_of_element_located((By.CLASS_NAME, class_name)))
            return captured_element
        elif css_selector:
            captured_element = WebDriverWait(browser, TIME_TO_WAIT).until(ec.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
            return captured_element
        else:
            print(f'Elemento não identificado')
    except Exception as e:
        print(f'Erro ao capturar elemento: {e}')
