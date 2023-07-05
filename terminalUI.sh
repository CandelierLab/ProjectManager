#!/bin/bash

# Script dir
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo 

while :
do

  python3 "$SCRIPT_DIR"/terminalUI.py disp home

  read -n1 -p "" key
  clear

  case $key in
    "p") 
      p=$(python3 "$SCRIPT_DIR"/terminalUI.py get path_programs)
      cd $p ;;
    "") break ;;
  esac

done

# clear