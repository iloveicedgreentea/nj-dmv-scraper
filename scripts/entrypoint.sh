#!/bin/bash

set -Eeou pipefail

# Run app 
if [[ "$1" == "start" ]]; then
  echo "Starting scrape"
  /usr/local/bin/start.sh

else
  exec "$@"
fi