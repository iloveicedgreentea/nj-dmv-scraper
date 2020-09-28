from os import getenv, path, mkdir
import datetime as DT
import csv
from bs4 import BeautifulSoup
import requests
import logging
import pytz
from sys import exit

logging.basicConfig(level=logging.INFO)

# CSV schema
csv_file_name = "output/data.csv"
csv_headers = ["location", "time_full", "date"]

# URL to parse
url = getenv("MAINSITE", "https://www.state.nj.us/mvc/locations/agency.htm")

# Get timestamp
eastern = pytz.timezone('US/Eastern')
today = DT.date.today()
# get utc now, convert to eastern TZ preserving DST
utc_now = DT.datetime.strptime(DT.datetime.now().strftime("%H:%M"), "%H:%M")
now = eastern.localize(utc_now).strftime("%H:%M")
weekday =  DT.datetime.today().weekday()

# dmv closes at 430 est on weekday
weekday_end_time = "16:30"
open_time = "8:00"
saturday_end_time = "15:00"

#check if sunday, dont run
if weekday == 6:
  print("No need to run on sunday :)")
  exit(0)

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

# parse site data
site_data = requests.get(url)
soup = BeautifulSoup(site_data.text, 'html.parser')

# get locations in red font, means they are full
full_locations = []
for item in soup.findAll(color="red"):
  full_locations.append(item.string)

# populate the list with all locations then remove the ones that are full
# todo: optimize this into one list comprehension
empty_locations = []
for item in soup.findAll("strong"):
  empty_locations.append(item.string)

for location in full_locations:
  if location in empty_locations:
    empty_locations.remove(location)



def check_rows(row, location, close_flag=False):
  # this will be really slow as the file gets bigger
    logging.debug(f"checking row {location}")
    logging.debug(f"{row[0]},{row[2]}")

    if close_flag:
      # If an entry was found return true
      if row[0] == location and "23:59" in row[1]:
        logging.debug("Entry already in database")
        return True
    else:
      # If an entry was found return true
      if row[0] == location and str(today) == row[2]:
        logging.debug("Entry already in database")
        return True

def check_if_open(now):
  if weekday == 5:
      if now > saturday_end_time and now > open_time and not entry_exists:
          return True
  # if weekday
  else:
    if now > weekday_end_time and now > open_time and not entry_exists:
        return True

# open csv for RW
with open(csv_file_name, 'r+', newline='') as file:
  writer = csv.writer(file)
  reader = csv.reader(file)
  
  # put this in a list so we can continuously iterate, otherwise it gets consumed in the first loop
  reader = list(reader)

  # list to hold new entries found in this run
  new_entries = []

  # first red element is the banner, skip it
  for location in full_locations[1:]:
    entry_exists = False
    
    # for each row in the current csv, check if the data was already written today
    for row in reader:
      if check_rows(row, location):
        entry_exists = True
        break

    # if the entry is not found, write it
    if not entry_exists:
      logging.info(f"New location detected: {location}")
      
      writer.writerow([location, now, today])
      new_entries.append(location)

  #if its the end of the day and an entry isn't present, write it as 23:59 to show it did not get full that day, but still have it for analytics
  # Also don't write a location if its closed, like at midnight
  entry_exists = False
  for location in empty_locations:
    for row in reader:
      if check_rows(row, location, close_flag=True):
        entry_exists = True
        break
    #todo: this isn't working
    if check_if_open(now) and not entry_exists:
      writer.writerow([location, "23:59", today])



logging.info(f"Locations added: {len(new_entries)}")
logging.info(f"Locations still open: {len(empty_locations)}")
logging.info(now)

#todo: see if its a vehicle or license center
#todo: twitter or some other kind of notification
