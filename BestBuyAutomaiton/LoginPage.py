from BestBuyAutomaiton.BasePage import BasePage
from Utils.BestBuyStrings import ACCOUNT_CLASS, ACCOUNT_SIGN_IN, SIGN_IN_USER, USERNAME_INPUT_CLASS
from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.support import expected_conditions as EC
import logging

logging.basicConfig(level=logging.INFO)


class LoginPage(BasePage):
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
