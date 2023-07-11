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

# === User interface =======================================================

L = project.ProjectsList()
P = L.getActiveProject()

match sys.argv[1]:

  case 'disp':

    # --- Initialization

    # Get terminal size
    tsz = os.get_terminal_size()

    # Get state
    state = sys.argv[2]
      
    sec = lambda title: ts.bDARKGREY + fix(' ' + title, tsz.columns) + ts.end
    sct = lambda s,d: ts.bBLUE + ' ' + s + ' ' + ts.end + ts.lightblue + ' ' + d + ts.end
    sctb = lambda s,d: ts.bDARKGREY + ' ' + s + ' ' + ts.end + ts.darkgrey + ' ' + d + ts.end
    scts = lambda s,d: ts.bGREEN + ' ' + s + ' ' + ts.end + ts.lightgreen + ' ' + d + ts.end
    spc = ' '*3

    # === Output generation ================================================

    # --- Header

    # Conda environment
    if P is None or P.conda is None:
      print(ts.bRED + fix(' ( ---- )', 10) + ts.end, end='')
      clen = 10
    else:
      print(ts.bGREEN + f' ({P.conda}) ' + ts.end, end='')
      clen = len(P.conda)+4

    # Project name
    if P is None:
      print(ts.bBLUE + fix(' --- No project selected ---', tsz.columns-clen) + ts.end)
    else:
      print(ts.bBLUE + fix(' ' + P.name, tsz.columns-clen) + ts.end)

    # Current path
    cpath = os.getcwd()

    if P is None:
      print(' ' + cpath)
    else:

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
      print(' '*(tsz.columns-42), sct('Back', 'Select project'), spc, sct('Return', 'Quit'))
    else:
      if P is None:
        print(' '*(tsz.columns-17), sct('Return', 'Quit'))
      else:
        print(' '*(tsz.columns-32), sct('Back', 'Home'), spc, sct('Return', 'Quit'))
    
    print('')

    match state:

      case 'home':
        ''' Home menu '''

        # --- Conda --------------------------------------------------------

        print(sec('Conda'))
        if P is None or P.conda is None:
          print(sct('a', fix('Activate', 17)), end='')
        else:
          print(sct('d', fix('Deactivate', 17)), end='')

        print(spc, sct('y', 'Export environment to .yml'))
        print(' '*24, sct('z', 'Reset environment from .yml'))
        print('')

        # --- Folders ------------------------------------------------------

        # Section title
        print(sec('Folders'))

        # Root
        print(sct('r', fix('Root', 17)), end='')

        # Programs
        if P is not None and P.programs is not None and os.path.isdir(P.programs):
          print(spc, sct('p', fix('Programs', 17)), end='')
        else:
          print(spc, sctb('p', fix('Programs', 17)), end='')

        # Spooler
        if P is not None and P.spooler is not None and os.path.isdir(P.spooler):
          print(spc, sct('s', fix('Spooler', 17)))
        else:
          print(spc, sctb('s', fix('Spooler', 17)))

        if P is not None and P.files is not None and os.path.isdir(P.files):
          print(sct('f', fix('Files', 17)))
        else:
          print(sctb('f', fix('Files', 17)))

        print('')

        # --- Git ----------------------------------------------------------

        # Section title
        print(sec('Git'))

        # 
        print(sct('§', fix('Push', 17)), end='')
        print(spc, sct('?', fix('Status', 17)), end='')
        print(spc, sct('c', fix('Commit', 17)))

        print(sct('!', fix('Pull', 17)))
        print('')

        # --- Documentation ------------------------------------------------
        print(sec('Documentation'))
        print(sct('h', 'Build html'))
        print('')

      case 'projects':
        ''' Projects menu '''

        #  Define  shortcuts
        L.setShortcuts()

        # Toolboxes
        print(sec('Toolboxes'))

        for i in L.list:
          if i.type=='toolbox':
            if i.isactive:
              print(scts(i.shortcut, i.name))
            else:
              print(sct(i.shortcut, i.name))

        print('')

        # Project list
        print(sec('Projects'))

        for i in L.list:
          if i.type=='project':
            if i.isactive:
              print(scts(i.shortcut, i.name))
            else:
              print(sct(i.shortcut, i.name))


        print('')

  case 'get':
      
    cmd = sys.argv[2]

    match cmd:

      case 'isAnyProjectSelected':
        print('False' if P is None else 'True')

      case 'name':
        print(P.name)

      case 'path_root': 
        print(P.path)

      case 'path_programs':
        print(P.programs)

      case 'path_spooler':
        print(P.spooler)

      case 'path_files':
        print(P.files)

  case 'select':

    # Get shortcut key
    key = sys.argv[2]

    #  Define  shortcuts
    L.setShortcuts()

    # --- Get project

    for item in L.list:

      if item.shortcut==key:
        L.toggleActiveState(item)
        break
    
    P = L.getActiveProject()
    
    # Update conda
    if P is None:
      print('conda deactivate')
    else:
      print(f'conda deactivate; conda activate {P.name}')