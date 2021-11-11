import csv

def fetch_proxy():
  with open('proxy.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        return row
