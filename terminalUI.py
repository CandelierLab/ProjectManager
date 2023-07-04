import os
from readchar import readkey, key

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
  ''' SEt string size (for tabular-like display) '''
  if len(s)>=l:
    return s[:l]
  else:
    return s + ' '*(l-len(s))

# --------------------------------------------------------------------------
class CurrentProject():

  def __init__(self):

    self.conda = 'Conda'
    self.name = 'Project Name'
    self.path = 'path/to/project'

# === Initialization =======================================================

state = 'menu'
P = CurrentProject()

# === MAIN LOOP ============================================================

while True:

  os.system('clear')

  # Get terminal size
  tsz = os.get_terminal_size()

  print(ts.bGREEN + f' ({P.conda}) ' + ts.end, end='')
  print(ts.bBLUE + fix(' ' + P.name, tsz.columns-len(P.conda)-4) + ts.end)
  print(ts.blue + ' ' + P.path + ts.end)
  print(' '*(tsz.columns-30), end='')
  print(ts.bBLUE + ' Return ' + ts.end + ts.lightblue + ' Quit' + ts.end + ' '*3, end='')
  print(ts.bBLUE + ' + ' + ts.end + ts.lightblue + ' Parameters' + ts.end)
  print('')

  # Conda
  print(ts.bDARKGREY + fix(' Conda', tsz.columns) + ts.end)
  print(ts.bBLUE + ' a ' + ts.bLIGHTBLUE + fix(' Activate', 17) + ts.end + ' '*3, end='')
  print(ts.bBLUE + ' r ' + ts.bLIGHTBLUE + fix(' Recreate environment from .yml', tsz.columns-26) + ts.end)
  print('')

  # Folders
  print(ts.bDARKGREY + fix(' Folders', tsz.columns) + ts.end)
  print(ts.bBLUE + ' p ' + ts.bLIGHTBLUE + fix(' Programs', 17) + ts.end + ' '*3, end='')
  print(ts.bBLUE + ' f ' + ts.bLIGHTBLUE + fix(' Files', 17) + ts.end + ' '*3, end='')
  print(ts.bBLUE + ' s ' + ts.bLIGHTBLUE + fix(' Spooler', 17) + ts.end)
  print('')

  # Git
  print(ts.bDARKGREY + fix(' Git', tsz.columns) + ts.end)
  print(ts.bBLUE + ' PageUp   ' + ts.bLIGHTBLUE + fix(' Push', 10) + ts.end + ' '*3, end='')
  print(ts.bBLUE + ' ? ' + ts.bLIGHTBLUE + fix(' Status', 17) + ts.end + ' '*3, end='')
  print(ts.bBLUE + ' c ' + ts.bLIGHTBLUE + fix(' Commit', 17) + ts.end)  
  print(ts.bBLUE + ' PageDown ' + ts.bLIGHTBLUE + fix(' Pull', 10) + ts.end)
  print('')

  # Documentation
  print(ts.bDARKGREY + fix(' Documentation', tsz.columns) + ts.end)
  print(ts.bBLUE + ' h ' + ts.bLIGHTBLUE + fix(' Build html', 17) + ts.end)
  print('')

  break

  match state:

    case 'menu':
      ''' Main menu '''
      
      k = readkey()

      match k:
        
        case key.ENTER:
          ''' Termination '''
          break

        case _:
          print(k)