from telnetlib import EC

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

link = "http://localhost:4200/"
browser = webdriver.Chrome()
browser.maximize_window()
browser.get(link)

search_string = browser.find_element(By.CSS_SELECTOR, "input[class*=ng-untouched]")
search_string.send_keys("Москва")


knop = browser.find_element(By.CSS_SELECTOR, "span[class*=material-symbols-outlined]").click()


test = WebDriverWait(browser,10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/town-finder/div/app-city-list/div/div/a/div[2]/h2"))).text

test_1 = "Москва"
assert test == test_1, f"Test not successful {test}"

browser.quit()
