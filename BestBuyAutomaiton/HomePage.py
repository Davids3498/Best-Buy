import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from BestBuyAutomaiton import BasePage
from Utils.BestBuyStrings import BEST_BUY_URL
from Utils.StateCode import Country
import logging


class HomePage(BasePage):
    def open(self):
        self.driver.get(BEST_BUY_URL)

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
