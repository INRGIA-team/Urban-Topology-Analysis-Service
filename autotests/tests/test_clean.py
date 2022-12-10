from selenium import webdriver
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

link = "http://localhost:4200/"
driver = webdriver.Chrome(executable_path='C:\\Urban-Topology-Analysis-Service-ui_api-integration\\autotests\\chromedriver\\chromedriver.exe')
driver.maximize_window()
driver.get(link)

write_string = "Москва"
string = driver.find_element(By.CSS_SELECTOR, "input[class*=ng-untouched]")
string.send_keys(write_string)
time.sleep(6)
string.clear()
time.sleep(10)


driver.quit()