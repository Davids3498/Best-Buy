import json
import random

from Utils.BestBuyStrings import USERS_JSON_PATH


def verify_word_in_suggestions(suggestions, word):
    return all(word in suggestion.lower() for suggestion in suggestions)


def clean_products_result(product_result):
    modified_product_result = [s.text.split('\n')[0] for s in product_result]
    return modified_product_result


def check_different_products(prodict_list1, prodict_list2):
    return prodict_list1 != prodict_list2


def load_user(user_path):
    """Load the JSON configuration file."""
    try:
        with open(user_path, 'r') as json_file:
            config_data = json.load(json_file)
        return config_data
    except FileNotFoundError:
        print(f"Error: {user_path} not found.")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return None

def get_random_user(user_path = USERS_JSON_PATH):
    config = load_user(user_path)
    if config and 'users' in config:
        return random.choice(config['users'])
    else:
        print("No users found in the configuration.")
        return None