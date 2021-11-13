import time
import requests
from config import settings

BASE_URL = 'https://sms-activate.ru/stubs/handler_api.php'

class SmsActivator:
  def __init__(self, country):
    self.country = country
    self.number = ""
    self.id = ""
    self.code = ""

  def get_number(self):
    params = {
      'api_key': settings.api_key,
      'action': 'getNumber',
      'service': 'go',
      'operator': 'any',
      'country': self.country['activator_index']
    }
    resp = requests.get(BASE_URL, params=params)
    print(resp.text)
    _, id, number = resp.text.split(':')
    self.number = number
    self.id = id
    self.__activate()
    return number

  def get_code(self):
    params = {
      'api_key': settings.api_key,
      'action': 'getStatus',
      'id': self.id
    }
    counter = 0
    while counter < settings.get_code_retries_max:
      resp = requests.get(BASE_URL, params=params)
      print(resp.text)
      if resp.text == 'STATUS_WAIT_CODE':
        counter += 1
        time.sleep(settings.get_code_retries_wait_sec)
      else:
        _, code = resp.text.split(':')
        self.code = code
        self.__complete_activation()
        return code

  def __activate(self):
    params = {
      'api_key': settings.api_key,
      'action': 'setStatus',
      'status': '1',
      'id': self.id
    }
    resp = requests.get(BASE_URL, params=params)
    print(resp.text)

  def __complete_activation(self):
    params = {
      'api_key': settings.api_key,
      'action': 'setStatus',
      'status': '6',
      'id': self.id
    }
    resp = requests.get(BASE_URL, params=params)
    print(resp.text)
