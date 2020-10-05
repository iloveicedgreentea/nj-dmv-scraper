#!/bin/bash

make build

while true; do
  make run
  sleep 180
done