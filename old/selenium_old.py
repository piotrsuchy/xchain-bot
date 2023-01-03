from selenium import webdriver
import time
# # do send keys
# from selenium.webdriver.common.keys import Keys
# # to wait until something loads
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

PATH = "C:\Program Files (x86)\chromedriver\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://xchain.io/")
# print(driver.title)
time.sleep(2)
button_dispenser = driver.find_element_by_link_text("Dispensers")
button_dispenser.click()

time.sleep(5)
#
# l = driver.find_elements_by_xpath("//*[@id='DataTables_Table_5']")

# hash = []
# block = []
# time_ = []
# source = []
asset_name = []
# cost = []
# view_button = []




for j in range(1, 10):
    xpath_1 = '//*[@id="DataTables_Table_5"]/tbody/tr[{}]/td[5]'.format(j)
    asset_name.append(driver.find_element_by_xpath(xpath_1).text)
# hash.append(hash_)
# print(hash_)
# block.append(match.find_element_by_xpath('./td[2]').text)
# time_.append(match.find_element_by_xpath('./td[3]').text)
# source.append(match.find_element_by_xpath('./td[4]').text)
# asset_name.append(match.find_element_by_xpath('./td[5]').text)
# cost.append(match.find_element_by_xpath('./td[6]').text)
# view_button.append(match.find_element_by_xpath('./td[7]').text)
print(asset_name)


time.sleep(2)


# print(hash)
# print(time_)
# # #if i wanted to click something after clicking the dispenser button
# # try:
# #     element = WebDriverWait(driver, 10).until(
# #         EC.presence_of_element_located((By.LINK_TEXT, "___")))
# # finally:
# #     driver.quit()
#
# time.sleep(10)

# button_dispenses = driver.find_element_by_link_text("Dispenses")
# button_dispenses.click()
#
time.sleep(5)
driver.quit()
