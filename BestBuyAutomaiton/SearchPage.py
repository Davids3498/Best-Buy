import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from BestBuyAutomaiton.BasePage import BasePage
from Utils.BestBuyStrings import FOR_PRODUCTS_CLASS, SEARCH_BAR_CLASS, SEARCH_COMPLETION_CLASS, SEARCH_COMPLETION_ITEM_CLASS
from Utils.GeneralFunction import clean_products_result
from selenium.webdriver.common.action_chains import ActionChains

import logging

logging.basicConfig(level=logging.INFO)


class SearchPage(BasePage):
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

    def get_completions(self):
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
            return []  # 