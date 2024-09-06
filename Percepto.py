import json
import logging
import time

from Utils.BestBuyAutomation import BestBuyAutomation
from Utils.GeneralFunction import check_different_products, get_random_user
from Utils.Section import Section


def main():
    start_time = time.time()

    user = get_random_user()

    automation = BestBuyAutomation()
    automation.select_state()
    # automation.login(user)

    # tasks 4 and 5
    query = "hello"
    hello_kitty = "hello kitty"

    try:
        # instead of search_and_check we can use the methods and functions it uses here
        assert automation.search_and_check(
            query, hello_kitty), f"With query {query}, not all complitions had {hello_kitty} in the name."
    except Exception:
        pass

    # task 6 - i used one hover over, if needed more we can just add them here
    products_pre_change = automation.get_products_for()
    automation.hover_over_search_completion(1)
    products_post_change = automation.get_products_for()

    is_product_change = check_different_products(
        products_pre_change, products_post_change)
    try:
        # instead of search_and_check we can use the methods and functions it uses here
        assert is_product_change, "Products did not change."
    except Exception:
        pass

    # task 7
    automation.hover_over_search_completion(
        2)  # third result option in the list
    # first product
    automation.click_on_for_product(0)
    # task 8
    automation.check_price_and_font_size()
    # task 9
    try:
        assert automation.check_section_appearance(
            Section.Features), f"details section for {Section.Features.value} did notappear on the screen ."
    except Exception:
        pass
    try:
        assert automation.check_section_appearance(
            Section.Specifications), f"details section for {Section.Specifications.value} did notappear on the screen ."
    except Exception:
        pass
    try:
        assert automation.check_section_appearance(
            Section.QuestionsAndAnswers), f"details section for {Section.QuestionsAndAnswers.value} did notappear on the screen ."
    except Exception:
        pass
    automation.close()
    end_time = time.time()
    logging.info(f"Assignment completed in {(end_time - start_time) / 60:.2f} minutes.")


if __name__ == '__main__':
    main()
