#!/bin/bash

# Script dir
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Default state
state="home"

# Default action
action=""

while :
do

  # Check project selection
  p=$(python3 "$SCRIPT_DIR"/terminalUI.py get isAnyProjectSelected)
  if [ "$p" == "False" ]
  then
    state="projects"
  fi
  
  # === DISPLAY ============================================================

  clear

  # --- Options

  python3 "$SCRIPT_DIR"/terminalUI.py disp "$state"

  # --- Actions

  if [ -n "$action" ]
  then
    echo -e "\e[90m$ $action\e[0m"
    eval $action
    action="" 
  fi

  # === INPUT ==============================================================

  # --- Get inputs

  read -sn1 key

  # --- Process input

  case $state in

    "home")

      case $key in

        $'\177')
          # --- Project selection
          state=$(echo 'projects') ;;

        "a") 
          # --- Conda: activate
          conda activate $(python3 "$SCRIPT_DIR"/terminalUI.py get name)
          ;;

        "d") 
          # --- Conda: deactivate
          conda deactivate
          ;;  

        "r") 
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
          
        "§")
          # --- Git push
          action="git push" ;;

        "!")
          # --- Git pull
          action="git pull" ;;

        "?") 
          # --- Git: Status
          action="git status" ;;

        "c") 
          # --- Git: Commit
          action="git commit" ;;

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

        *)
          # --- Select project
          res=$(python3 "$SCRIPT_DIR"/terminalUI.py select "$key")
          eval $res
          ;;

      esac ;;

  esac

done

# clear