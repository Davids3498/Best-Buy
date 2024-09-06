import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utils import Section
from Utils.BestBuyStrings import ACCOUNT_CLASS, ACCOUNT_SIGN_IN, BEST_BUY_URL, BODY, FOR_PRODUCTS_CLASS, POPUP_SECTION_CLASS, PRICE_CLASS, SEARCH_BAR_CLASS, SEARCH_COMPLETION_CLASS, SEARCH_COMPLETION_ITEM_CLASS, SIGN_IN_USER, TIME_OUT, USERNAME_INPUT_CLASS
from Utils.GeneralFunction import clean_products_result, verify_word_in_suggestions
from selenium.webdriver.common.action_chains import ActionChains
from Utils.StateCode import Country

import logging

logging.basicConfig(level=logging.INFO)


class BestBuyAutomation:
    def __init__(self):
        self.driver = webdriver.Chrome()  # Setup WebDriver
        self.driver.get(BEST_BUY_URL)
        self.wait = WebDriverWait(self.driver, TIME_OUT)

    def select_state(self, state_code: Country = Country.US):
        """Selects a state."""
        try:
            self.wait.until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, f"{state_code.value}-link"))
            ).click()
            logging.info(f"{state_code} site selected.")
        except Exception as e:
            logging.error(f"Error selecting {state_code}: {e}")

    def login(self, user: dict):
        """Login to a user"""
        try:
            self.wait.until(
                EC.element_to_be_clickable((By.ID, ACCOUNT_CLASS))
            ).click()

            self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, ACCOUNT_SIGN_IN))
            ).click()

            self.wait.until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME, USERNAME_INPUT_CLASS))
            )
            email_input = self.driver.find_elements(By.CLASS_NAME, USERNAME_INPUT_CLASS)[
                0]  # First input is email
            email_input.send_keys(user['username'])

            password_input = self.driver.find_elements(By.CLASS_NAME, USERNAME_INPUT_CLASS)[
                1]  # Second input is password
            password_input.send_keys(user['password'])

            sign_in_button = self.driver.find_element(
                By.CLASS_NAME, SIGN_IN_USER)
            sign_in_button.click()

            # TODO: add skip if the website asks for a phone number - can not implement because it asks for verification which i dont have

            logging.info("Login successful.")
        except Exception as e:
            logging.error(f"Error during login: {e}")

    def search(self, query: str):
        """Search for a query in the search bar."""
        try:
            # Wait for the search bar to be visible and enter the query
            search_bar = self.wait.until(
                EC.visibility_of_element_located((By.ID, SEARCH_BAR_CLASS))
            )
            search_bar.send_keys(query)

            logging.info(f"Searched for: {query}")
        except Exception as e:
            logging.error(f"Error during search: {e}")

    def _get_completions(self):
        """Get all completions"""
        try:
            # Wait  or the completions dropdown to be visible
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.ID, SEARCH_COMPLETION_CLASS))
            )

            suggestions = self.driver.find_elements(
                By.CSS_SELECTOR, SEARCH_COMPLETION_ITEM_CLASS
            )

            modified_suggestions = clean_products_result(suggestions)
            return modified_suggestions

        except Exception as e:
            logging.error(f"Error getting search completions: {e}")
            return []  # Return an empty list in case of failure

    def search_and_get_completions(self, query: str):
        """Seach for a query and return the completions for that query."""
        self.search(query)
        return self._get_completions()

    def search_and_check(self, query: str, word_to_check: str):
        """Performs the search and checks if a specific word is present in all suggestions."""
        suggestions = self.search_and_get_completions(query)
        if suggestions:
            return verify_word_in_suggestions(suggestions, word_to_check)
        else:
            logging.info("No suggestions found.")

    def get_products_for(self):
        """Get all 'Product for' for a hover"""
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.ID, SEARCH_COMPLETION_CLASS))
            )

            suggestions = self.driver.find_elements(
                By.CSS_SELECTOR, FOR_PRODUCTS_CLASS)

            modified_suggestions = clean_products_result(suggestions)
            return modified_suggestions

        except Exception as e:
            logging.error(f"Error getting 'Products for' suggestions: {e}")
            return []  # Return an empty list in case of failure

    def hover_over_search_completion(self, index: int):
        """Hovers over an element index in the search bar completion drop down menu"""
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.ID, SEARCH_COMPLETION_CLASS))
            )

            suggestions = self.driver.find_elements(
                By.CSS_SELECTOR, SEARCH_COMPLETION_ITEM_CLASS)

            if index < len(suggestions):
                # Hover over the suggestion at the given index
                actions = ActionChains(self.driver)
                actions.move_to_element(suggestions[index]).perform()
                time.sleep(0.5)  # so the for products will fully load

            else:
                logging.info(
                    f"Index {index} is out of range. There are only {len(suggestions)} suggestions.")

        except Exception as e:
            logging.info(f"Error during hover action: {e}")

    def click_on_for_product(self, index: int):
        """Clicks on a product from the right side of the search bar drop menu."""
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.ID, SEARCH_COMPLETION_CLASS))
            )
            suggestions = self.driver.find_elements(
                By.CSS_SELECTOR, FOR_PRODUCTS_CLASS)
            if index < len(suggestions):
                suggestions[index].click()
            else:
                logging.info(
                    f"Index {index} is out of range. There are only {len(suggestions)} suggestions.")
            return True

        except Exception as e:
            logging.error(f"Error during clicking on product: {e}")
            return False

    def check_price_and_font_size(self, font_size: str = '30px'):
        """Check the font size of the price element."""
        try:
            price_span = self._get_price_element()
            price_text = price_span.text

            if price_text:
                actual_font_size = price_span.value_of_css_property(
                    "font-size")
                return font_size == actual_font_size

        except Exception as e:
            logging.error(f"Error checking font size: {e}")
            return False

    def _get_price_element(self):
        """Get the price element of a product."""
        try:
            price_element = self.wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, PRICE_CLASS))
            )

            price_span = price_element.find_element(By.TAG_NAME, "span")
            return price_span

        except Exception as e:
            logging.error(f"Error checking font size: {e}")
            return None

    def click_section(self, section: Section):
        """Clicks on the specified section and checks if the detail section appears."""
        section_name = section.value
        try:
            if section_name == "Features":
                section_button_xpath = "//button[contains(@class, 'features-drawer-btn')]//span[text()='Features']"
            elif section_name == "Specifications":
                section_button_xpath = "//button[contains(@class, 'specifications-drawer-btn')]//h2[text()='Specifications']"
            elif section_name == "Questions & Answers":
                section_button_xpath = "//button[contains(@class, 'c-button-unstyled')]//span/span[contains(text(), 'Questions & Answers')]"
            else:
                logging.error(f"Section {section_name} not found")
                return False

            section_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, section_button_xpath))
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView();", section_button)
            time.sleep(0.5)  # Wait 500 milliseconds

            self.driver.execute_script("arguments[0].click();", section_button)

            popup_visible = self.wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, POPUP_SECTION_CLASS))  # Pop-up class
            )

            return popup_visible

        except Exception as e:
            print(f"Error while checking {section.value} section: {e}")

    def check_section_appearance(self, section: Section):
        """Checks if section pop appears nad close it"""
        is_visiable = self.click_section(section)
        if is_visiable:
            self.click_outside_to_close_popup()
            return True
        return False

    def click_outside_to_close_popup(self):
        """Clicks outside the popup to close it."""
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.TAG_NAME, BODY))
            )
            outside_element = self.driver.find_element(By.TAG_NAME, BODY)
            outside_element.click()
            time.sleep(0.5)

        except Exception as e:
            print(f"Error closing popup: {e}")

    def close(self):
        try:
            self.driver.quit()
        except Exception as e:
            logging.error(f"Error closing WebDriver: {e}")
