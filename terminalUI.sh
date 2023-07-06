#!/bin/bash

# Script dir
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Default state
state=$(echo 'projects')

while :
do

  python3 "$SCRIPT_DIR"/terminalUI.py disp "$state"

  read -n1 -p "" key
  clear

  case $state in

    "home")

      case $key in

        $'\177')
          # --- Project selection
          state=$(echo 'projects') ;;

        "p") 
          # --- Folder: Root
          p=$(python3 "$SCRIPT_DIR"/terminalUI.py get path_root)
          cd $p ;;

        "p") 
          # --- Folder: Programs
          p=$(python3 "$SCRIPT_DIR"/terminalUI.py get path_programs)
          cd $p ;;

        "s") 
          # --- Folder: Spooler
          p=$(python3 "$SCRIPT_DIR"/terminalUI.py get path_spooler)
          cd $p ;;

        "f") 
          # --- Folder: Files
          p=$(python3 "$SCRIPT_DIR"/terminalUI.py get path_files)
          cd $p ;;

        "") 
          # --- Quit
          break ;;

      esac ;;

    "projects")

      case $key in

        $'\177')
          # --- Back to home
          state=$(echo 'home') ;;

        "") 
          # --- Quit
          break ;;

      esac ;;

  esac

done

# clear