import random

COUNTRIES = [
  {'activator_index': '0', 'gmail_prefix': 'Россия (+7)'},
  # {'activator_index': '1', 'gmail_prefix': 'Украина (+380)'}
]

def pick_country():
  sample = random.choice(COUNTRIES)
  print(f'Got country: {sample}')
  return sample
