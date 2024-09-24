from BestBuyAutomaiton.BasePage import BasePage
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Utils import Section
from Utils.BestBuyStrings import BODY, POPUP_SECTION_CLASS, PRICE_CLASS
import logging

logging.basicConfig(level=logging.INFO)

class ProductPage(BasePage):
    def get_price_font_size(self):
        try:
            price_span = self._get_price_element()
            if price_span:
                return price_span.value_of_css_property("font-size")
            else:
                return None
        except Exception as e:
            logging.error(f"Error checking font size: {e}")
            return None

    def _get_price_element(self):
        try:
            price_element = self.wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, PRICE_CLASS))
            )
            price_span = price_element.find_element(By.TAG_NAME, "span")
            return price_span
        except Exception as e:
            logging.error(f"Error finding price element: {e}")
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

    def close_popup(self):
        try:
            outside_element = self.driver.find_element(By.TAG_NAME, BODY)
            outside_element.click()
        except Exception as e:
            print(f"Error closing popup: {e}")