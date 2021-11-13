import time
from config import settings
from random import randint
from random import sample
from faker import Faker
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from password_generator import PasswordGenerator
from sms_activator import SmsActivator
from csv_proxy_fetcher import fetch_proxy
from countries import pick_country

START_URL = "https://accounts.google.com/signup/v2/webcreateaccount?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&flowName=GlifWebSignIn&flowEntry=SignUp"

def main():
  password_generator = PasswordGenerator()
  password_generator.minlen = settings.password_length
  profile = webdriver.FirefoxProfile()
  profile.set_preference("media.peerconnection.enabled", False)
  (ip, port, login, password, _) = fetch_proxy()
  proxy_options = {
    'proxy': {
      'http': f'socks5://{login}:{password}@{ip}:{port}',
      'https': f'socks5://{login}:{password}@{ip}:{port}',
      'no_proxy': f'socks5://{login}:{password}@{ip}:{port}'
    }
  }
  driver = webdriver.Firefox(profile, seleniumwire_options=proxy_options)
  driver.get(START_URL)
  __start(driver, password_generator)


def __start(driver, password_generator):
  fake = Faker()
  first_name = fake.first_name()
  last_name = fake.last_name()
  name = "".join(sample([first_name, last_name], 2))
  random_number = randint(100, 10000)
  user_name = f'{name}{random_number}'.lower()
  password = password_generator.generate()
  __fill_basic_info_and_proceed(driver, first_name, last_name, user_name, password)
  time.sleep(settings.step_wait_sec)

  country = pick_country()
  activator = SmsActivator(country)
  number = activator.get_number()
  __fill_phone_number_and_proceed(driver, country, number)
  time.sleep(settings.step_wait_sec)

  code = activator.get_code()
  __fill_code_and_proceed(driver, code)
  time.sleep(settings.step_wait_sec)

  __fill_birthday_and_proceed(driver)
  time.sleep(settings.step_wait_sec)

  driver.find_element_by_xpath("//span[text() = 'Пропустить']").click();
  time.sleep(settings.step_wait_sec)

  driver.find_element_by_xpath("//span[text() = 'Принимаю']").click();
  time.sleep(settings.step_wait_sec)
  WebDriverWait(driver, 100).until(EC.title_contains(f'{user_name}@gmail.com'))
  print(f"DONE: {user_name}@gmail.com {password}")

def __fill_basic_info_and_proceed(driver, first_name, last_name, user_name, password):
  driver.find_element(By.NAME, 'firstName').send_keys(first_name)
  driver.find_element(By.NAME, "lastName").send_keys(last_name)
  driver.find_element(By.NAME, "Username").send_keys(user_name)
  driver.find_element(By.NAME, "Passwd").send_keys(password)
  driver.find_element(By.NAME, "ConfirmPasswd").send_keys(password, Keys.ENTER)

def __fill_phone_number_and_proceed(driver, country, number):
  gmail_prefix = country['gmail_prefix']
  driver.find_element(By.ID, "countryList").click()
  driver.find_element_by_xpath(f"//span[text() = '{gmail_prefix}']").click()
  driver.find_element(By.ID, "phoneNumberId").clear()
  driver.find_element(By.ID, "phoneNumberId").send_keys(number, Keys.ENTER)

def __fill_code_and_proceed(driver, code):
  driver.find_element(By.ID, "code").send_keys(code, Keys.ENTER)

def __fill_birthday_and_proceed(driver):
  month = str(randint(1, 12))
  driver.execute_script(f'document.getElementById("month").value = {month}')
  driver.execute_script('document.getElementById("gender").value = "1"')
  driver.find_element(By.ID, "day").send_keys(str(randint(1, 28)))
  driver.find_element(By.ID, "year").send_keys(str(randint(1980, 2010)), Keys.ENTER)

if __name__ == "__main__":
  main()
