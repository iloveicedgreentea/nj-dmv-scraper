from logging import info
from os import getenv, path, mkdir
from datetime import date, datetime
import csv
from bs4 import BeautifulSoup
import requests
import logging

logging.basicConfig(level=logging.INFO)

# CSV schema
csv_file_name = "output/data.csv"
csv_headers = ["location", "time_full", "date"]

# URL to parse
url = getenv("MAINSITE", "https://www.state.nj.us/mvc/locations/agency.htm")

# check if csv exists, create csv with headers if not
if not path.exists(csv_file_name):
  logging.info("CSV not found, creating...")
  try:
    mkdir(path.dirname(csv_file_name))
  except FileExistsError:
    pass
  with open(csv_file_name, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_headers)

# Get timestamp
today = date.today()
now = datetime.now().strftime("%H:%M")

# parse site data
site_data = requests.get(url)
soup = BeautifulSoup(site_data.text, 'html.parser')

# get locations in red font, means they are full
full_locations = soup.findAll(color='red')
# open csv for RW
with open(csv_file_name, 'r+', newline='') as file:
  writer = csv.writer(file)
  reader = csv.reader(file)
  
  # put this in a list so we can continuously iterate, otherwise it gets consumed in the first loop
  reader = list(reader)

  new_entries = []

  # read each row, check if the entry already exists

  # first element is the banner
  for location in full_locations[1:]:
    entry_exists = False
    # for each row in the current csv, check if the data was already written today
    for row in reader:
    # this will be really slow as the file gets bigger
      logging.debug(f"checking row {location.string}")
      logging.debug(f"{row[0]},{row[2]}")
      # If an entry was found, exit the loop
      if row[0] == location.string and str(today) == row[2]:
        logging.debug("Entry already in database")
        entry_exists = True
        break
        
    if not entry_exists:
      logging.info(f"New location detected: {location.string}")
      writer.writerow([location.string, now, today])
      new_entries.append(location.string)

logging.info(f"Locations added: {len(new_entries)}")

#todo: see if its a vehicle or license center
#todo: twitter or some other kind of notification