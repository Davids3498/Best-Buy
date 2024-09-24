from selenium.webdriver.support.ui import WebDriverWait

from Utils.BestBuyStrings import TIME_OUT


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIME_OUT)
