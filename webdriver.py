from selenium import webdriver
from selenium_stealth import stealth

def get_selenium_webdriver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    prefs = {"download.default_directory" : "."}
    options.add_experimental_option('prefs',prefs)
    
    driver = webdriver.Chrome('chromedriver', options=options)
    
    if headless:
        stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Win32", webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True)
    
    return driver
