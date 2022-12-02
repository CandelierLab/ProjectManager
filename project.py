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

# --- Active toolboxes and projects ----------------------------------------

def get_active(available_toolboxes=None, available_projects=None):
  '''
  Get the list of active toolboxes and projects
  '''

  # Incomplete input
  if available_toolboxes is None or available_projects is None:
    available_toolboxes, available_projects = get_available()

  tact = {}
  pact = {}

  with open(root+'/ACTIVE') as f:
    lines = f.read().splitlines()

  for line in lines:

    if line=='':
      continue

    # Toolbox
    if line in available_toolboxes:
      tact[available_toolboxes.index(line)] = line

    # Project
    if line in available_projects:
      pact[available_projects.index(line) + len(available_toolboxes)] = line

  return tact, pact

# === PROJECT SELECTOR =====================================================

class Selector:
  '''
  The toolbox/project selector class
  '''

  HEADER = '\033[95m'
  BLUE = '\033[94m'
  CYAN = '\033[96m'
  GREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

  def display_item(self, p, k):

    # Decide color based on activation state
    if p in self.active_toolboxes.values():
      color = self.GREEN + self.BOLD + self.UNDERLINE
    elif p in self.active_projects.values():
      color = self.BLUE + self.BOLD + self.UNDERLINE
    else:
      color = '' #tcolor.BLUE

    p_ = os.path.basename(p) + self.ENDC + ' '*(15-len(os.path.basename(p)))
    print('  {:s}: {:s} {:s}'.format(
      '{:s}{:d}{:s}'.format(color, k, self.ENDC),
      color + p_ + self.ENDC,
      color + p + self.ENDC))

    return k+1
    
  def __init__(self):

    self.available_toolboxes, self.available_projects = get_available()
    self.active_toolboxes, self.active_projects = get_active(self.available_toolboxes, self.available_projects)

    # --- Display

    msg = ''

    while True:

      # Clear terminal
      os.system('clear')

      # Message
      print(msg)

      # Index identifier
      k = 0

      # Toolboxes
      print(self.CYAN + 'TOOLBOXES' + self.ENDC)

      for p in self.available_toolboxes:
        k = self.display_item(p, k)

      # Projects
      print('\n' + self.CYAN + 'PROJECTS' + self.ENDC)

      for p in self.available_projects:
        k = self.display_item(p, k)

      print('Enter: Quit')

      c = input('?> ')
      
      match c:
        case '':
          k = None
          break
        case _:
          if c.isdigit() and int(c)<k:
            k = int(c)
            break
          else:
            msg = "\n{:s}The input '{:s}' is unclear. Please try again.{:s}\n".format(self.WARNING, c, self.ENDC)
      
    # --- Update active items

    if k is not None:
      
      # --- Toolboxes

      if k in self.active_toolboxes:

        # Inactivate toolbox
        self.active_toolboxes.pop(k)

      elif k in self.active_projects:

        # Inactivate project
        self.active_projects.pop(k)

      elif k<len(self.available_toolboxes):

        # Activate toolbox
        self.active_toolboxes[k] = self.available_toolboxes[k]

      else:

        # Activate project
        self.active_projects = {k: self.available_projects[k-len(self.available_toolboxes)]}

      # --- Update ACTIVE file

      with open(root+'/ACTIVE', 'w') as f:
        for p in self.active_toolboxes.values():
          f.write(p.strip() + '\n')
        for p in self.active_projects.values():
          f.write(p.strip() + '\n')

      # --- Update display
      Selector()

# === MAIN ENTRY POINT =====================================================

if __name__ == '__main__':

  Selector()