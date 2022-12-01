import os

# === DEFINITIONS ==========================================================

# Project manager's root
root = os.path.dirname(os.path.realpath(__file__))

# --- List of available projects -------------------------------------------

def get_available():
  '''
  Get the list of available projects
  '''

  with open(root+'/LOCATIONS') as f:
    lines = f.read().splitlines()

  # Lists
  mode = None
  tlist = []
  plist = []

  for path in lines:
    
    match path:
      case '': 
        continue
      case '## Toolboxes':
        mode = 'toolbox'
        continue
      case '## Projects':
        mode = 'project'
        continue

    if mode is not None:

      line = [path]

      while len(line):

        # Current path under investigation
        cur = line.pop(0)

        if 'Programs' in os.listdir(cur):
          if 'Python' in os.listdir(os.path.join(cur,'Programs')):
            match mode:
              case 'toolbox':
                tlist.append(cur)
              case 'project':
                plist.append(cur)

        else:
          for entry in os.scandir(cur):
            if entry.is_dir():
              line.append(os.path.join(cur,entry.name))

  return tlist, plist

available_toolboxes, available_projects = get_available()

# --- Active toolboxes and projects ----------------------------------------

def get_active():
  '''
  Get the list of active toolboxes and projects
  '''

  tact = {}
  pact = {}

  with open(root+'/ACTIVE') as f:
    lines = f.read().splitlines()

  for line in lines:

    # Toolbox
    if line in available_toolboxes:
      tact[available_toolboxes.index(line)] = line

    # Project
    if line in available_projects:
      pact[available_projects.index(line) + len(available_toolboxes)] = line

  return tact, pact

active_toolboxes, active_projects = get_active()

# with open(root+'/CURRENT') as f:
#   lines = f.read().splitlines()

# === PROJECT SELECTOR =====================================================

class tcolor:
  HEADER = '\033[95m'
  BLUE = '\033[94m'
  CYAN = '\033[96m'
  GREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

if __name__ == '__main__':
  '''
  MAIN
  '''

  # --- Display

  msg = ''

  while True:

    # Clear terminal
    # os.system('clear')

    # Message
    print(msg)

    k = 0

    # Toolboxes
    print('TOOLBOXES')

    for p in available_toolboxes:
      p_ = os.path.basename(p) + ' '*(15-len(os.path.basename(p)))
      print('  {:s}: {:s} {:s}'.format(
        '{:s}{:s}{:d}{:s}'.format(tcolor.CYAN, tcolor.BOLD,k, tcolor.ENDC),
        tcolor.CYAN+tcolor.BOLD+p_+tcolor.ENDC,
        p))
      k+=1

    # Projects
    print('\nPROJECTS')

    for p in available_projects:

      # Decide color based on activation state
      if p in active_projects.values():
        color = tcolor.GREEN
      else:
        color = tcolor.BLUE

      p_ = os.path.basename(p) + ' '*(15-len(os.path.basename(p)))
      print('  {:s}: {:s} {:s}'.format(
        '{:s}{:s}{:d}{:s}'.format(color, tcolor.BOLD,k, tcolor.ENDC),
        color + tcolor.BOLD + p_ + tcolor.ENDC,
        p))
      k+=1

    print('{:s}: {:s}'.format(
      '{:s}{:s}{:s}{:s}'.format(tcolor.BLUE, tcolor.BOLD, 'Enter', tcolor.ENDC),
      tcolor.BLUE+tcolor.BOLD+ 'Quit' +tcolor.ENDC))

    # c = input('?> ')
    c = ''
    
    match c:
      case '':
        break
      case _:
        if c.isdigit() and int(c)<len(available_projects):
          i = int(c)
          break
        else:
          msg = "\n{:s}The input '{:s}' is unclear. Please try again.{:s}\n".format(tcolor.WARNING, c, tcolor.ENDC)
    
    # --- Current project info
    # print(plist[i])
