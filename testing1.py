from selenium import webdriver
from selenium.webdriver.common.by import By
import time
driver = webdriver.Chrome()

driver.get("https://vantageglobalprime-pty-vuk-live.onezero.com:44300/Dashboard")
driver.find_element(By.XPATH,'//*[@id="Username"]').send_keys("RegionalControl")
driver.find_element(By.XPATH,'//*[@id="Password"]').send_keys("Risk:readonly777")
driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/form/input[1]').click()
driver.find_element(By.XPATH,'//*[@id="globalNavigationBar"]/div/ul/li[2]/div/ul/li/a').click()
time.sleep(20)
driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div/div/div[1]/div/div/span').click()
time.sleep(1)
driver.find_element(By.XPATH,'//*[@id="settingsPullDown-list"]/span/input').send_keys("Symbol")
time.sleep(2)
driver.find_element(By.XPATH,'//*[@id="settingsPullDown_listbox"]/li').click()
time.sleep(3)
driver.find_element(By.XPATH,'//*[@id="d6f0c44c-e4d5-457e-9a3d-0381e03ff18e"]/a').click()
time.sleep(1)
driver.find_element(By.XPATH,'/html/body/div[15]/form/div[1]/input[1]').send_keys("XAU/USD")
time.sleep(1)
driver.find_element(By.XPATH,'/html/body/div[15]/form/div[1]/div[2]/button[1]').click()
time.sleep(60)
