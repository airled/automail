import sys
import time
from config import settings
from random import randint, sample, choice
from faker import Faker
from password_generator import PasswordGenerator
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# custom libs
from sms_activator import SmsActivator
from user_agent import get_user_agent
from csv_proxy_fetcher import fetch_proxy
from countries import pick_country

START_URL = "https://accounts.google.com/signup/v2/webcreateaccount?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&flowName=GlifWebSignIn&flowEntry=SignUp"

def main():
  number_of_emails = int(sys.argv[1])
  for i in range(0, number_of_emails):
    __run()


def __run():
  password_generator = PasswordGenerator()
  password_generator.minlen = settings.password_length
  profile = webdriver.FirefoxProfile()
  # hide webrtc
  profile.set_preference("media.peerconnection.enabled", False)
  profile.set_preference("general.useragent.override", get_user_agent())
  driver = webdriver.Firefox(profile, seleniumwire_options=fetch_proxy())
  driver.get(START_URL)
  (email, password) = __start(driver, password_generator)
  f = open("result.txt", "a")
  f.write(f'{email} {password}\n')
  f.close()
  driver.close()

def __start(driver, password_generator):
  fake = Faker()
  first_name = fake.first_name()
  last_name = fake.last_name()
  name = "".join(sample([first_name, last_name], 2))
  random_number = randint(1000, 10000)
  user_name = f'{name}{random_number}'.lower()
  password = password_generator.generate()
  __fill_basic_info_and_proceed(driver, first_name, last_name, user_name, password)
  __wait_for_step()

  country = pick_country()
  activator = SmsActivator(country)
  number = activator.get_number()
  __fill_phone_number_and_proceed(driver, country, number)
  __wait_for_step()

  code = activator.get_code()
  __fill_code_and_proceed(driver, code)
  __wait_for_step()

  __fill_birthday_and_proceed(driver)
  __wait_for_step()

  driver.find_element_by_xpath("//span[text() = 'Пропустить']").click();
  __wait_for_step()

  driver.find_element_by_xpath("//span[text() = 'Принимаю']").click();
  __wait_for_step()
  WebDriverWait(driver, 100).until(EC.title_contains(f'Входящие'))
  print(f"DONE: {user_name}@gmail.com {password}")
  return (f'{user_name}@gmail.com', password)

def __fill_basic_info_and_proceed(driver, first_name, last_name, user_name, password):
  driver.find_element(By.NAME, 'firstName').send_keys(first_name)
  __wait_for_fill()
  driver.find_element(By.NAME, "lastName").send_keys(last_name)
  __wait_for_fill()
  driver.find_element(By.NAME, "Username").send_keys(user_name)
  __wait_for_fill()
  driver.find_element(By.NAME, "Passwd").send_keys(password)
  __wait_for_fill()
  driver.find_element(By.NAME, "ConfirmPasswd").send_keys(password, Keys.ENTER)

def __fill_phone_number_and_proceed(driver, country, number):
  gmail_prefix = country['gmail_prefix']
  if country['activator_index'] != '0':
    driver.find_element(By.ID, "countryList").click()
    driver.find_element_by_xpath(f'(//span[text()="{gmail_prefix}"][last()])').click()
  driver.find_element(By.ID, "phoneNumberId").clear()
  __wait_for_fill()
  driver.find_element(By.ID, "phoneNumberId").send_keys(number, Keys.ENTER)

def __fill_code_and_proceed(driver, code):
  driver.find_element(By.ID, "code").send_keys(code, Keys.ENTER)

def __fill_birthday_and_proceed(driver):
  month = str(randint(1, 12))
  driver.execute_script(f'document.getElementById("month").value = {month}')
  __wait_for_fill()
  driver.execute_script('document.getElementById("gender").value = "1"')
  __wait_for_fill()
  driver.find_element(By.ID, "day").send_keys(str(randint(1, 28)))
  __wait_for_fill()
  driver.find_element(By.ID, "year").send_keys(str(randint(1980, 2000)), Keys.ENTER)

def __wait_for_step():
  sec_range = range(settings.step_wait_min_sec, settings.step_wait_max_sec + 1)
  time.sleep(choice(sec_range))

def __wait_for_fill():
  sec_range = range(settings.fill_wait_min_sec, settings.fill_wait_max_sec + 1)
  time.sleep(choice(sec_range))

if __name__ == "__main__":
  main()
