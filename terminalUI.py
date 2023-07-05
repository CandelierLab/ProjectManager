import os
import sys

import project

# --------------------------------------------------------------------------
class ts:
  ''' Define terminal styling'''
  
  end = '\033[0m'
  bold = '\033[01m'
  disable = '\033[02m'
  underline = '\033[04m'
  reverse = '\033[07m'
  strikethrough = '\033[09m'
  invisible = '\033[08m'

  black = '\033[30m'
  red = '\033[31m'
  green = '\033[32m'
  orange = '\033[33m'
  blue = '\033[34m'
  purple = '\033[35m'
  cyan = '\033[36m'
  lightgrey = '\033[37m'
  darkgrey = '\033[90m'
  lightred = '\033[91m'
  lightgreen = '\033[92m'
  yellow = '\033[93m'
  lightblue = '\033[94m'
  pink = '\033[95m'
  lightcyan = '\033[96m'

  bBLACK = '\033[40m'
  bRED = '\033[41m'
  bGREEN = '\033[42m'
  bORANGE = '\033[43m'
  bBLUE = '\033[44m'
  bLIGHTBLUE = '\033[104m'
  bPURPLE = '\033[45m'
  bCYAN = '\033[46m'
  bLIGHTGREY = '\033[47m'
  bDARKGREY = '\033[100m'

# --------------------------------------------------------------------------
def fix(s, l):
  ''' Set string size (for tabular-like display) '''
  if l is None:
    return s
  elif len(s)>=l:
    return s[:l]
  else:
    return s + ' '*(l-len(s))

# --------------------------------------------------------------------------
class CurrentProject():

  def __init__(self):
    
    self.path = project.root
    self.name = os.path.basename(os.path.normpath(project.root))
    self.conda = os.environ['CONDA_DEFAULT_ENV'] if 'CONDA_DEFAULT_ENV' in os.environ else None

match sys.argv[1]:

  case 'disp':

    # --- Initialization

    os.system('clear')

    # Get terminal size
    tsz = os.get_terminal_size()

    # Get state
    state = sys.argv[2]
      
    sec = lambda title: ts.bDARKGREY + fix(' ' + title, tsz.columns) + ts.end
    sct = lambda s,d: ts.bBLUE + ' ' + s + ' ' + ts.end + ts.lightblue + ' ' + d + ts.end
    scts = lambda s,d: ts.bGREEN + ' ' + s + ' ' + ts.end + ts.lightgreen + ' ' + d + ts.end
    spc = '  '

    # === Output generation ================================================

    # --- Header

    P = CurrentProject()

    # Conda environment
    if P.conda is None:
      print(ts.bRED + fix(' ( ---- )', 10) + ts.end, end='')
      clen = 10
    else:
      print(ts.bGREEN + f' ({P.conda}) ' + ts.end, end='')
      clen = len(P.conda)+4

    # Project name
    print(ts.bBLUE + fix(' ' + P.name, tsz.columns-clen) + ts.end)

    # Current path
    cpath = os.getcwd()

    inter = []
    for i in range(min(len(cpath), len(P.path))):
      if cpath[i]==P.path[i]:
        inter += cpath[i]
      else:
        i -= 1
        break

    i += 1
    print(ts.green +  ' ' + cpath[:i] + ts.end, end='')

    if i>=len(P.path):
      print(cpath[i:])
    else:
      print(ts.red +  cpath[i:] + ts.end)

    # General options
    print('')
    if state=='home':
      print(' '*(tsz.columns-60), sct('Back', 'Select project'), end='')
    else:
      print(' '*(tsz.columns-50), sct('Back', 'Home'), end='')
    
    print(spc, sct('Return', 'Quit'), spc, sct('+', 'Parameters'))
    print('')

    match state:

      case 'home':
        ''' Home menu '''

        # Conda
        print(sec('Conda'))
        if P.conda is None:
          print(sct('a', fix('Activate', 17)), '', end='')
        else:
          print(sct('d', fix('Deactivate', 17)), '', end='')

        print(spc, sct('y', 'Export environment to .yml'))
        print(' '*24, sct('z', 'Reset environment from .yml'))
        print('')

        # Folders
        print(sec('Folders'))
        print(sct('p', fix('Programs', 17)), spc, sct('f', fix('Files', 17)), spc, sct('s', fix('Spooler', 17)))
        print('')

        # Git
        print(sec('Git'))
        print(sct('PageUp  ', fix('Push', 10)), spc, sct('?', fix('Status', 17)), spc, sct('c', fix('Commit', 17)))
        print(sct('PageDown', fix('Pull', 10)))
        print('')

        # Documentation
        print(sec('Documentation'))
        print(sct('h', 'Build html'))
        print('')

      case 'projects':
        ''' Projects menu '''

        available_toolboxes, available_projects = project.get_available()
        active_toolboxes, active_projects = project.get_active(available_toolboxes, available_projects)
        
        # Toolboxes
        print(sec('Toolboxes'))
        
        k = 1

        for p in available_toolboxes:

          if p in active_toolboxes.values():
            print(scts('{:02d}'.format(k), os.path.basename(p)))
          else:
            print(sct('{:02d}'.format(k), os.path.basename(p)))

          k += 1

        print('')

        # Project list
        print(sec('Projects'))

        for p in available_projects:

          if p in active_projects.values():
            print(scts('{:02d}'.format(k), os.path.basename(p)))
          else:
            print(sct('{:02d}'.format(k), os.path.basename(p)))

          k += 1

        print('')


  case 'get':
      
    cmd = sys.argv[2]

    match cmd:
      case 'path_programs': 
        P = CurrentProject()
        print(P.path + '/Programs/Python')

      case 'path_spooler': 
        P = CurrentProject()
        print(P.path + '/Programs/Python/Spooler')

      case 'path_files': 
        P = CurrentProject()
        print(P.path + '/Files')