import pytest
from BestBuyAutomaiton.BestBuyAutomation import BestBuyAutomation
from Utils.BestBuyStrings import AUTO_COMPLETE_PRODUCT_LIST, USERS
from Utils.GeneralFunction import check_different_products, get_random_user
from Utils.Section import Section
from Utils.StateCode import Country


@pytest.fixture()
def automation() -> BestBuyAutomation:
    return BestBuyAutomation()


@pytest.mark.parametrize('user', USERS)
def test_login(automation: BestBuyAutomation, user):
    automation.open_home_page()
    automation.select_state()
    automation.login(user)


@pytest.mark.parametrize('state', [Country.US, Country.CANADA])
def test_select_state(automation: BestBuyAutomation, state):
    automation.open_home_page()
    automation.select_state(state)


@pytest.mark.parametrize('product', AUTO_COMPLETE_PRODUCT_LIST)
def test_auto_complition(automation: BestBuyAutomation, product):
    automation.open_home_page()
    automation.select_state()
    automation.login(get_random_user)
    search_word = product['search_word']
    complition = product['complition']
    assert automation.search_and_check(
        search_word, complition), f"With query {search_word}, not all complitions had {complition} in the name."


def test_hover_on_complition_product_and_check_related_products_change(automation: BestBuyAutomation):
    automation.open_home_page()
    automation.select_state()
    automation.login(get_random_user)
    products_pre_change = automation.search_page.get_products_for()
    automation.hover_over_search_completion(1)
    products_post_change = automation.search_page.get_products_for()
    assert check_different_products(products_pre_change, products_post_change)


def test_product(automation: BestBuyAutomation):
    automation.open_home_page()
    automation.select_state()
    automation.login(get_random_user)
    automation.hover_over_search_completion(
        2)  # third result option in the list
    # first product
    automation.click_on_for_product(0)
    # task 8
    automation.get_price_font_size()
    # task 9
    for section in [Section.Features, Section.Specifications, Section.QuestionsAndAnswers]
    assert automation.check_section_appearance(
        section), f"details section for {section.value} did not appear on the screen ."
