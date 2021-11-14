import random
from fake_user_agent.main import user_agent

ALLOWED_BROWSERS = [
  'chrome',
  'firefox',
  'safari'
]

def get_user_agent():
  browser = random.choice(ALLOWED_BROWSERS)
  ua = user_agent(browser)
  print(f'Using user-agent {ua}')
  return ua
