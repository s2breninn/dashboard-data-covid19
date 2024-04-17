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

def get_element_data(url, **kwargs):
    TIME_TO_WAIT = 10

    # Example
    # options = '--headless', '--disable-gpu'
    options = ()
    browser = make_chrome_browser(*options)

    browser.get(url)

    # Espere para encontrar o input
    for arg, value in kwargs.items():
        if arg == 'xpath':
            return WebDriverWait(browser, TIME_TO_WAIT).until(ec.presence_of_element_located((By.XPATH, value)))
        elif arg == 'link_text':
            return WebDriverWait(browser, TIME_TO_WAIT).until(ec.presence_of_element_located((By.LINK_TEXT, value)))
        elif arg == 'partial_link_text':
            return WebDriverWait(browser, TIME_TO_WAIT).until(ec.presence_of_element_located((By.PARTIAL_LINK_TEXT, value)))
        elif arg == 'tag_name':
            return WebDriverWait(browser, TIME_TO_WAIT).until(ec.presence_of_element_located((By.TAG_NAME, value)))
        elif arg == 'class_name':
            return WebDriverWait(browser, TIME_TO_WAIT).until(ec.presence_of_element_located((By.CLASS_NAME, value)))
        elif arg == 'css_selector':
            return WebDriverWait(browser, TIME_TO_WAIT).until(ec.presence_of_element_located((By.CSS_SELECTOR, value)))
        else:
            print("Invalid selection method.")

'''    search_input.send_keys('Hello world')
    search_input.send_keys(Keys.ENTER)

    results = browser.find_element(By.ID, 'search')
    links = results.find_elements(By.TAG_NAME, 'a')
    links[0].click()
    print(links)

    # Dorme por 10s
    sleep(TIME_TO_WAIT)'''