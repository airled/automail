import sys
import time
from config import settings
from random import randint, sample, choice
from faker import Faker
from password_generator import PasswordGenerator
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire.undetected_chromedriver import Chrome, ChromeOptions
# custom libs
from csv_proxy_fetcher import fetch_proxy
from sms_activator import SmsActivator
from countries import pick_country

START_URL = "https://accounts.google.com/signup/v2/webcreateaccount?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&flowName=GlifWebSignIn&flowEntry=SignUp"

def main():
  number_of_emails = int(sys.argv[1])
  for i in range(0, number_of_emails):
    __run_browser()


def __run_browser():
  options = ChromeOptions()
  options.add_argument('--no-first-run')
  options.add_extension('/home/air/projects/automail/webrtc-control.crx')
  options.add_extension('/home/air/projects/automail/random-useragent.crx')
  driver = Chrome(seleniumwire_options=fetch_proxy(), options=options)
  driver.request_interceptor = __intercept_request
  driver.get(START_URL)
  (email, password) = __start_steps(driver)
  f = open("result.txt", "a")
  f.write(f'{email} {password}\n')
  f.close()
  driver.close()

def __intercept_request(request):
  del request.headers['Proxy-Connection']

def __start_steps(driver):
  fake = Faker()
  first_name = fake.first_name()
  last_name = fake.last_name()
  user_name = "".join(sample([
    first_name,
    last_name,
    str(randint(1000, 10000))
  ], 3)).lower()
  print(f'Username: {user_name}')
  password_generator = PasswordGenerator()
  password_generator.minlen = settings.password_length
  password = password_generator.generate()
  print(f'Password: {password}')
  __fill_basic_info_and_proceed(driver, first_name, last_name, user_name, password)
  __wait_for_step()

  country = pick_country()
  activator = SmsActivator(country)

  __fill_phone_number_and_proceed(driver, country, activator.get_number())
  __wait_for_step()

  __fill_code_and_proceed(driver, activator.get_code())
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
