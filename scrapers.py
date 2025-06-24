import os
from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _init_driver() -> webdriver.Chrome:
    """Initializes a Chrome WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    return webdriver.Chrome(options=options)


def fetch_total_coto(produtos: List[str]) -> float:
    """Logs into Coto Digital, adds products to the cart and returns the total."""
    dni = os.getenv("COTO_DNI")
    password = os.getenv("COTO_PASSWORD")
    if not dni or not password:
        raise ValueError("Coto credentials not configured")

    driver = _init_driver()
    wait = WebDriverWait(driver, 10)
    total = 0.0
    try:
        driver.get("https://www.cotodigital.com.ar/sitios/cdigi/")

        # Login process
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.login-btn"))).click()
        wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(dni)
        wait.until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys(password + Keys.RETURN)

        # Search and add each product
        for produto in produtos:
            search = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.search")))
            search.clear()
            search.send_keys(produto)
            search.send_keys(Keys.RETURN)
            add = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.add-to-cart")))
            add.click()

        # Go to cart and read the total cost
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.cart"))).click()
        total_text = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.total-price"))).text
        total = float(total_text.replace("$", "").replace(",", "."))
    finally:
        driver.quit()

    return total


def fetch_total_carrefour(produtos: List[str]) -> float:
    """Logs into MiCarrefour, adds products to the cart and returns the total."""
    email = os.getenv("CARREFOUR_EMAIL")
    password = os.getenv("CARREFOUR_PASSWORD")
    if not email or not password:
        raise ValueError("Carrefour credentials not configured")

    driver = _init_driver()
    wait = WebDriverWait(driver, 10)
    total = 0.0
    try:
        driver.get("https://www.carrefour.com.ar/")

        # Login process
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.login"))).click()
        wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys(email)
        wait.until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys(password + Keys.RETURN)

        # Search and add each product
        for produto in produtos:
            search = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.search")))
            search.clear()
            search.send_keys(produto)
            search.send_keys(Keys.RETURN)
            add = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.add-to-cart")))
            add.click()

        # Go to cart and read the total cost
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.cart"))).click()
        total_text = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.total-price"))).text
        total = float(total_text.replace("$", "").replace(",", "."))
    finally:
        driver.quit()

    return total