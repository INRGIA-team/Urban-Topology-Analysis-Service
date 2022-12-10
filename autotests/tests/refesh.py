from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

link = "http://localhost:4200/"
browser =webdriver.Chrome(executable_path='C:\\Urban-Topology-Analysis-Service-ui_api-integration\\autotests\\chromedriver\\chromedriver.exe')
browser.maximize_window()
browser.get(link)

error_city_search = "Москво"

string = browser.find_element(By.CSS_SELECTOR, "input[class*=ng-untouched]")
string.send_keys(error_city_search)

knop = browser.find_element(By.CSS_SELECTOR, "span[class*=material-symbols-outlined]").click()

right_city_search = "Москва"
assert error_city_search == f"Test not successful "

browser.refresh()
time.sleep(5)
browser.quit()