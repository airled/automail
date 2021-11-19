import sys
import time
from config import settings
from random import randint, sample, choice
from faker import Faker
from password_generator import PasswordGenerator
from seleniumwire.undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# custom libs
from csv_proxy_fetcher import fetch_proxy
from filler import Filler
from countries import pick_country
from sms_activator import SmsActivator

START_URL = "https://accounts.google.com/signup/v2/webcreateaccount?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&flowName=GlifWebSignIn&flowEntry=SignUp"

def main():
  number_of_emails = int(sys.argv[1])
  for i in range(0, number_of_emails):
    run_browser()


def run_browser():
  options = ChromeOptions()
  options.add_argument('--no-first-run')
  options.add_extension('/home/air/projects/automail/webrtc-control.crx')
  options.add_extension('/home/air/projects/automail/random-useragent.crx')
  options.add_extension('/home/air/projects/automail/Canvas-Fingerprint-Defender.crx')
  options.add_extension('/home/air/projects/automail/Font-Fingerprint-Defender.crx')
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
  password_generator.minlen = settings.password_minimal_length
  password = password_generator.generate()
  print(f'Password: {password}')

  filler = Filler(driver)

  filler.fill_basic_info(first_name, last_name, user_name, password)
  __wait_for_step()

  country = pick_country()
  activator = SmsActivator(country)

  filler.fill_phone_number(country, activator.get_number())
  __wait_for_step()

  filler.fill_code(activator.get_code())
  __wait_for_step()

  filler.fill_birthday()
  __wait_for_step()

  driver.find_element_by_xpath("//span[text() = 'Пропустить']").click();
  __wait_for_step()

  driver.find_element_by_xpath("//span[text() = 'Принимаю']").click();
  __wait_for_step()

  WebDriverWait(driver, 100).until(EC.title_contains(f'Входящие'))
  print(f"DONE: {user_name}@gmail.com {password}")
  return (f'{user_name}@gmail.com', password)

def __wait_for_step():
  sec_range = range(settings.step_wait_min_sec, settings.step_wait_max_sec + 1)
  time.sleep(choice(sec_range))

if __name__ == "__main__":
  main()
