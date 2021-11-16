import csv
import random

def fetch_proxy():
  with open('proxy.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    # TODO: temporary logic. will be replaced in future
    (ip, port, login, password, _) = random.choice(list(reader))
    print(f'Using proxy: {login}:{password}@{ip}:{port}')
    return {
      'proxy': {
        'http': f'socks5://{login}:{password}@{ip}:{port}',
        'https': f'socks5://{login}:{password}@{ip}:{port}',
        'no_proxy': f'socks5://{login}:{password}@{ip}:{port}'
      }
    }
