# NJ MVC/DMV Scraper

This is a rudimentary scraper for the NJ DMV to check when locations get full.

It writes data to a CSV - location, time it was detected to be full, and the date. 

The CSV can be used to graph how busy a DMV location is over time. I made this to quickly see which DMV to go to.


## Getting started

Requirements: Docker, Bash

Run app in docker:
`make build`

`make run`

This will output the CSV in the `output` folder

## Local development

`make setup`

## Analysis

Analyse how early in the day locations got full

Which DMVs fill up the fastest, correlates to how busy they are