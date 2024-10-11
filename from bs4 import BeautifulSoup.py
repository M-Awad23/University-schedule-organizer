from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException as ECIE, NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import pandas as pd
import requests
import csv
import time


driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
driver.get("https://regapp.ju.edu.jo/regapp/login.xhtml")

username_field = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='اسم المستخدم']"))
)
password_field = WebDriverWait(driver, 5).until(
     EC.presence_of_element_located((By.XPATH, "//input[@placeholder='كلمة السر']"))
)
captcha_field = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='رمز التحقق']"))
)

student_id = input("Enter your student ID: ")
password = input("Enter your password: ")
captcha_code = input("Enter the security code: ")
username_field.send_keys(student_id)
password_field.send_keys(password)
captcha_field.send_keys(captcha_code)
captcha_field.send_keys(Keys.RETURN)

driver.get("https://regapp.ju.edu.jo/regapp/secured/course-schedule-plan.xhtml")
driver.execute_script("document.body.style.zoom='25%'")

file_path = 'C:\\Users\\Mohammed\\Desktop\\codes\\data.csv' #my path; change to yours
    
with open(file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    for i in range(8):
        try:
            header = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, f"j_idt36:{i}:j_idt37_header"))
            )
            header.click()
            time.sleep(1)
        except (NoSuchElementException, TimeoutException):
            print("No more headers found")
            break
            
        for x in range(50):
            try:
                button = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, f"j_idt36:{i}:coursedatatable:{x}:j_idt47"))
                )
                button.click()
                time.sleep(1)

                dialog_title = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.ID, "dialog_title"))
                ).text
                print(f"Scraping data for course: {dialog_title}")
                writer.writerow([f"Course: {dialog_title}"])

            
                table = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[role='dialog']"))
                )

                table_html = table[0].get_attribute('outerHTML')
                soup = BeautifulSoup(table_html, 'html.parser')

                rows = soup.find_all('tr')

                for row in rows:
                    headers = row.find_all('th')
                    if headers:
                        header_data = [header.text.strip() for header in headers]
                        writer.writerow(header_data)
                    else:    
                        cols = row.find_all('td')
                        col_data = [col.text.strip() for col in cols]
                        writer.writerow(col_data)



                close = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".ui-dialog-titlebar-close"))   
                    )
                close.click()
                time.sleep(1)

            except (NoSuchElementException, TimeoutException):
                print(f"No more buttons found in section {i+1} after {x+1} buttons.")
                break







       








