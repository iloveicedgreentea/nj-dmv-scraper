# NJ MVC/DMV Scraper

This is a rudimentary scraper for the NJ DMV to check when locations get full.

It writes data to a CSV - location, time it was detected to be full, and the date. 

The CSV can be used to graph how busy a DMV location is over time. I made this to quickly see which DMV to go to.

This is designed to run as a scheduled job, as quickly as you want before you get IP banned. 


* I am not responsible for anything anyone does with this. See `LICENSE` for details.

* The MVC does a horrible job of updating the site so expect the locations to have closed over an hour before getting marked as full. They seem to get pushed in batches, probably manually. 

* To the best of my knowledge and research, this does not violate any ToS on the NJ state website. Don't prosecute me because you didn't think to provide a public API for this.


## Getting started

Requirements: Docker, Bash

Run app in docker:

`make build`

`make run`

This will output the CSV in the `output` folder

Run `run.sh` for a simple script that will poll every 30s

## Local development

`make setup`

`source .venv/bin/activate`

`python src/main.py`

## Analysis Examples

* Analyze how early in the day locations got full

* Which DMVs fill up the fastest, correlates to how busy they are relative to each other

* Which days are busiest