import time
from random import choice, randint
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class Filler:
  def __init__(self, driver):
    self.driver = driver

  def fill_basic_info(self, first_name, last_name, user_name, password):
    self.__fill(By.NAME, 'firstName', first_name, Keys.TAB)
    self.__fill(By.NAME, 'lastName', last_name, Keys.TAB)
    self.__fill(By.NAME, 'Username', user_name, Keys.TAB)
    self.__fill(By.NAME, 'Passwd', password, Keys.TAB)
    self.__fill(By.NAME, 'ConfirmPasswd', password, Keys.ENTER)

  def fill_phone_number(self, country, number):
    gmail_prefix = country['gmail_prefix']
    if country['activator_index'] != '0':
      self.driver.find_element(By.ID, "countryList").click()
      self.driver.find_element_by_xpath(f'(//span[text()="{gmail_prefix}"][last()])').click()
    self.driver.find_element(By.ID, "phoneNumberId").clear()
    self.__fill(By.ID, 'phoneNumberId', number, Keys.ENTER)

  def fill_code(self, code):
    self.__fill(By.ID, 'code', code, Keys.ENTER)

  def fill_birthday(self):
    month = str(randint(1, 12))
    self.__fill(By.ID, 'day', str(randint(1, 28)))
    self.driver.execute_script(f'document.getElementById("month").value = {month}')
    self.driver.execute_script('document.getElementById("gender").value = "1"')
    self.__fill(By.ID, "year", str(randint(1980, 2000)), Keys.ENTER)

  def __fill(self, selector, field, value, key=None):
    element = self.driver.find_element(selector, field)
    chars = list(value)
    for char in chars:
      element.send_keys(char)
      sleep_for = choice(range(1, 5)) / 10
      time.sleep(sleep_for)
    if key is not None:
      element.send_keys(key)
