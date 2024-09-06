# Best Buy Automation Developer Assignment

This project is an automation script built using **Python** and **Selenium** to perform various tasks on the Best Buy website. The script is part of an automation developer assignment and includes tasks such as logging in, searching for items, interacting with product sections, and checking page elements.

## Table of Contents
- [Setup](#setup)
- [How to Run](#how-to-run)
- [Task Overview](#task-overview)
- [Project Structure](#project-structure)
- [Notes](#notes)

## Setup

### Prerequisites
- Python 3.x
- Google Chrome browser
- ChromeDriver (ensure ChromeDriver version matches your installed Chrome version)
- Selenium Python library

### Install Dependencies
To install the required Python libraries, run the following command in the project directory:
```bash
pip install -r requirements.txt
```
Also chrome driver needs to be installed:
```bash
sudo apt install chromium-chromedriver
```

## How To Run
Clone the repo and run
```bash
python main.py
```

## Task Overview

The script automates the following tasks:

1. **Open Best Buy website**: Navigate to [www.bestbuy.com](https://www.bestbuy.com).
2. **Select the USA site**: Ensure that the USA region is selected when opening the website.
3. ~~**Login to the system**: Login to Best Buy using one of the provided credentials from a list.~~
4. **Search for "hello"**: Perform a search using the keyword "hello" and verify that all the returned results contain the phrase "hello kitty".
5. **Hover over product sections**: Hover over different options in the "Products for" section and verify that the content of this section changes accordingly.
6. **Navigate to a specific product**: Go to the first product on the third result option in the search results list.
7. **Check price and font size**: On the product page, verify that a price is displayed and that the font size of the price is 30px.
8. **Interact with the product details**: Click on the "Features", "Specifications", and "Questions & Answers" sections, ensuring that the respective details sections are displayed on the screen.

The login could not be made because authentication was needed.

## Project Structure

```
.
├── main.py                   # Main script to run the automation
├── README.md                 
├── requirements.txt          # Python dependencies
├── Utils
│   ├── BestBuyAutomation.py  # Class for automation interactions
│   ├── BestBuyStrings.py     # Constants for element identifiers
│   ├── GeneralFunction.py    # Helper functions for product checks
│   ├── Section.py            # Enum for the different sections
│   ├── StateCode.py          # Enum for country codes
|   └── Users.json            # User credentials for Best Buy login
└──
```

## Notes

 - The login process may sometimes ask for a phone number verification, which is not implemented in this version. If the website requests a phone number, a verification step is required that cannot be skipped in this implementation.
 - The assignment took approximately 5 hours to complete.
