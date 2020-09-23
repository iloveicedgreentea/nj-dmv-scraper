#!/bin/bash

make build

while true; do
  make run
  sleep 30
done