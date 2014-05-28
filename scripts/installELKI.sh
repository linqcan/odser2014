#!/bin/bash
# Checks if ELKI 0.6 is "installed". If not, it is downloaded and "installed".

# Try find out where we are
if [[ -f pipeline.py ]]; then
  cd ..
fi

if [[ ! -d bin/ ]]; then
  echo "Please run this script from the top folder or scripts folder"
  exit
fi

cd bin
if [[ ! -f elki.jar ]]; then
  curl "http://elki.dbs.ifi.lmu.de/releases/release0.6.0/elki.jar" -o "elki.jar"
else
  echo "ELKI is already installed!"
  exit
fi

if [[ -f elki.jar ]]; then
  echo "ELKI was downloaded and installed!"
fi
