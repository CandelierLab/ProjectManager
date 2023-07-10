import os

# === DEFINITIONS ==========================================================

# Project manager's root
manager_root = os.path.dirname(os.path.realpath(__file__))

# === PROJECTS LIST ========================================================

class ProjectItem():

  def __init__(self, type, path):

    # --- Main properties

    # Type
    # NB: can be 'project' or 'toolbox'
    self.type = type    

    # Absolute path
    self.path = path

    # Name
    self.name = os.path.basename(self.path)

    # Active status
    self.isactive = False

    # --- Generic paths

    # Programs
    p = self.path + '/Programs/Python'
    self.programs = p if os.path.isdir(p) else None

    # Spooler
    p = self.path + '/Programs/Python/Spooler'
    self.spooler = p if os.path.isdir(p) else None

    # Files
    p = self.path + '/Files'
    self.files = p if os.path.isdir(p) else None

    # --- Conda

    self.conda = os.environ['CONDA_DEFAULT_ENV'] if 'CONDA_DEFAULT_ENV' in os.environ else None

    # --- Misc UI properties
     
    self.shortcut = None
   
class ProjectsList():

  def __init__(self):
    
    # --- Available items --------------------------------------------------

    self.list = []

    with open(manager_root+'/LOCATIONS') as f:

      lines = f.read().splitlines()

      # Lists
      mode = None

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
                    self.list.append(ProjectItem('toolbox', cur))
                  case 'project':
                    self.list.append(ProjectItem('project', cur))

            else:
              for entry in os.scandir(cur):
                if entry.is_dir():
                  line.append(os.path.join(cur, entry.name))

    # --- Active items -----------------------------------------------------

    with open(manager_root+'/ACTIVE') as f:

      lines = f.read().splitlines()

      for item in self.list:
        if item.path in lines:
          item.isactive = True

  def check_source(self, source_file):

    from pathlib import PurePath
    from logging import error 

    if PurePath(source_file).is_relative_to(manager_root): return

    check = False
    for p in self.list:
      if PurePath(source_file).is_relative_to(p.path):
        check = True
        break

    if not check:
      try:
        raise Exception("\033[93mThe running script is not in the active project.\033[0m\nPlease run 'projects' in the terminal to select the correct project.")
      except BaseException as exception:
        error(f"{exception}")
        sys.exit()

  def getActiveProject(self):
    ''' Get the active project '''

    for i in self.list:
      if i.type=='project' and i.isactive: return i

    return None
  
  def toggleActiveState(self, p):
    ''' Toggle the active state of a project/toolbox '''

    with open(manager_root+'/ACTIVE', 'w') as f:

      for item in self.list:

        # Active state
        if item==p:
          item.isactive = not item.isactive
        elif p.type=='project' and item.type=='project':
          item.isactive = False

        # Save to file
        if item.isactive:
          f.write(item.path + '\n')
  
  def setShortcuts(self):

    # Shortcut reservoir
    R =  list(map(chr, range(97, 123))) + list(map(chr, range(65, 91))) + list(map(chr, range(48, 58)))

    # Items to assign
    U = list(range(len(self.list)))

    k = 0
    while len(U):

      V = []
      for i in U:

        item = self.list[i]

        # Digit (last resort)
        if k>=len(item.name):
          for j in range(9):
            if str(j) in R:
              item.shortcut = str(j)
              R.remove(item.shortcut)
              break
          else:
            continue
          continue

        # Lowercase letter
        if item.name[k].lower() in R:
          item.shortcut = item.name[k].lower()
          R.remove(item.shortcut)
          continue

        # Uppercase letter
        if item.name[k].upper() in R:
          item.shortcut = item.name[k].upper()
          R.remove(item.shortcut)
          continue

        V.append(i)

      U = V
      k += 1

# class Selector:
#   '''
#   The toolbox/project selector class
#   '''

#   HEADER = '\033[95m'
#   BLUE = '\033[94m'
#   CYAN = '\033[96m'
#   GREEN = '\033[92m'
#   WARNING = '\033[93m'
#   FAIL = '\033[91m'
#   ENDC = '\033[0m'
#   BOLD = '\033[1m'
#   UNDERLINE = '\033[4m'

#   def display_item(self, p, k):

#     # Decide color based on activation state
#     if p in self.active_toolboxes.values():
#       color = self.GREEN + self.BOLD + self.UNDERLINE
#     elif p in self.active_projects.values():
#       color = self.BLUE + self.BOLD + self.UNDERLINE
#     else:
#       color = '' #tcolor.BLUE

#     p_ = os.path.basename(p) + self.ENDC + ' '*(15-len(os.path.basename(p)))
#     print('  {:s}: {:s} {:s}'.format(
#       '{:s}{:d}{:s}'.format(color, k, self.ENDC),
#       color + p_ + self.ENDC,
#       color + p + self.ENDC))

#     return k+1
    
#   def __init__(self):

#     self.available_toolboxes, self.available_projects = get_available()
#     self.active_toolboxes, self.active_projects = get_active(self.available_toolboxes, self.available_projects)

#     # --- Display

#     msg = ''

#     while True:

#       # Clear terminal
#       # os.system('clear')

#       # Message
#       print(msg)

#       # Index identifier
#       k = 0

#       # Toolboxes
#       print(self.CYAN + 'TOOLBOXES' + self.ENDC)

#       for p in self.available_toolboxes:
#         k = self.display_item(p, k)

#       # Projects
#       print('\n' + self.CYAN + 'PROJECTS' + self.ENDC)

#       for p in self.available_projects:
#         k = self.display_item(p, k)

#       print('Enter: Quit')

#       c = input('?> ')
      
#       match c:
#         case '':
#           k = None
#           break
#         case _:
#           if c.isdigit() and int(c)<k:
#             k = int(c)
#             break
#           else:
#             msg = "\n{:s}The input '{:s}' is unclear. Please try again.{:s}\n".format(self.WARNING, c, self.ENDC)
      
#     # --- Update active items

#     if k is not None:
      
#       # --- Toolboxes

#       if k in self.active_toolboxes:

#         # Inactivate toolbox
#         self.active_toolboxes.pop(k)

#       elif k in self.active_projects:

#         # Inactivate project
#         self.active_projects.pop(k)

#       elif k<len(self.available_toolboxes):

#         # Activate toolbox
#         self.active_toolboxes[k] = self.available_toolboxes[k]

#       else:

#         # Activate project
#         self.active_projects = {k: self.available_projects[k-len(self.available_toolboxes)]}

#       # --- Update ACTIVE file

#       with open(manager_root+'/ACTIVE', 'w') as f:
#         for p in self.active_toolboxes.values():
#           f.write(p.strip() + '\n')
#         for p in self.active_projects.values():
#           f.write(p.strip() + '\n')

#       # --- Update display
#       Selector()

# === MAIN ENTRY POINT =====================================================

if __name__ == '__main__':

  P = ProjectsList()

  print(P.list)

  # Direct call: start the selector
  # Selector()

else:

  # Call as a module: check path

  import sys
  from inspect import getouterframes
  
  # Definitions
  items = ProjectsList()
  source_file = getouterframes(sys._getframe(1), 1)[-1].filename

  # --- Check if ipython3 or if source file belongs to the active project

  if os.path.normpath(source_file).split(os.sep)[-1] != 'ipython3':    
    items.check_source(source_file)

  # --- Import active item

  for item in items.list:

    if item.isactive:

      sys.path.append(item.path + '/Programs/Python')

      # Define root
      if item.type == 'project': root = item.path

    elif item.path+'/Programs/Python' in sys.path:

      sys.path.remove(item.path + '/Programs/Python')