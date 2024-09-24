import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from BestBuyAutomaiton.HomePage import HomePage
from BestBuyAutomaiton.LoginPage import LoginPage
from BestBuyAutomaiton.ProductPage import ProductPage
from BestBuyAutomaiton.SearchPage import SearchPage
from Utils import Section
from Utils.BestBuyStrings import ACCOUNT_CLASS, ACCOUNT_SIGN_IN, BEST_BUY_URL, BODY, FOR_PRODUCTS_CLASS, POPUP_SECTION_CLASS, PRICE_CLASS, SEARCH_BAR_CLASS, SEARCH_COMPLETION_CLASS, SEARCH_COMPLETION_ITEM_CLASS, SIGN_IN_USER, TIME_OUT, USERNAME_INPUT_CLASS
from Utils.GeneralFunction import clean_products_result, verify_word_in_all_suggestions
from selenium.webdriver.common.action_chains import ActionChains
from Utils.StateCode import Country

import logging

logging.basicConfig(level=logging.INFO)


class BestBuyAutomation:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.home_page = HomePage(self.driver)
        self.login_page = LoginPage(self.driver)
        self.search_page = SearchPage(self.driver)
        self.product_page = ProductPage(self.driver)

    def open_home_page(self):
        self.home_page.open()

    def select_state(self, state_code: Country = Country.US):
        self.home_page.select_state(state_code)

    def login(self, user):
        self.login_page.login(user)
        
    def __del__(self):
        self.close()
    
    def hover_over_search_completion(self, index: int):
        self.search_page.hover_over_search_completion(index)

    def click_on_for_product(self, index: int):
        return self.search_page.click_on_for_product(index)

    def get_price_font_size(self, font_size='30px'):
        actual_font_size = self.product_page.get_price_font_size()
        return actual_font_size == font_size

    def check_section_appearance(self, section):
        is_visible = self.product_page.click_section(section)
        if is_visible:
            self.product_page.close_popup()
            return True
        return False

    def search_and_get_completions(self, query):
        self.search_page.search(query)
        return self.search_page.get_completions()

    def search_and_check(self, query, word_to_check):
        suggestions = self.search_and_get_completions(query)
        if suggestions:
            return verify_word_in_all_suggestions(suggestions, word_to_check)
        else:
            logging.info("No suggestions found.")
            return False

    def close(self):
        try:
            self.driver.quit()
        except Exception as e:
            logging.error(f"Error closing WebDriver: {e}")
