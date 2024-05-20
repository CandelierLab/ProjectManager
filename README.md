# ProjectManager for Python

ProjectManager is a Python3 module easing the management of a collection of scientific projects and toolboxes.

Projects and toolboxes are simply directories with whatever architecture, the only constraint being that it must contain a `Settings` and `Programs/Python` folder/subfolder. For instance, a valid project could be:

```
project
  ├── Settings        ☚ Mandatory
  ├── Programs        ☚ Mandatory
  │   ├── Python      ☚ Mandatory. All the rest is optional
  │   │   └── ...
  │   ├── C++
  │   └── ...
  ├── Figures
  │   └── ...
  ├── Movies
  ├── Files
  ├── Bibliography
  └── Documents
```

Projects and toolbox can then be activated (and deactivated) *via* a command-line interface. Activating a project means that, upon `import project`:  
* The `Programs/Python` subfolder is automatically appended to `sys.path`. This way all the programs in the nested architecture have access to the project's packages and modules without having to manually append the root path.
* The project's root path is accessible *via* `project.root`, which is useful for I/O operations relative to the project like saving/loading data files or figures in folders dissociated from the code itself.

> Note: Projects and toolboxes share the same architecture pattern. The only difference is that **there can be only one active project** while **multiple toolboxes can be activated at the same time**, alongside of the eventual current project.

## Installation and setup

### Debian/Ubuntu

1) Clone/download the files in the directory of your choice (e.g. `~/Science/Tools/ProjectManager`)

2) Permanently add the ProjectManager's `project` module to the PYTHONPATH. Add the following line at the end of `~/.bashrc:`

```
export PYTHONPATH=$PYTHONPATH:/path/to/ProjectManager
```

3) Add an alias for the project's selector CLI. In `~/.bash_aliases`, add:

```
alias projects='. /path/to/ProjectManager/terminalUI.sh
```

4) Restart your terminal.

5) Define where the projects and toolboxes are located by modifying the LOCATIONS file:
```
## Toolboxes
/home/user/Science/Toolboxes

## Projects
/home/user/Science/Projects
```

There can be multiple locations (one per line) in each section. In these directories, only the folders containing the `Programs/Python` architecture are  recognized as valid toolboxes and projects. The search is recursive though, so the actual project location can be nested in a subfolder structure.

## Usage

### Activate toolboxes and projects *via* the CLI

Type `projects` in the terminal to access the CLI:

```
TOOLBOXES
  0: TBox            /home/user/Science/Toolboxes/TBox

PROJECTS
  1: Proj1           /home/user/Science/Projects/AE/Proj1
  2: Proj2           /home/user/Science/Projects/AE/Proj2
  3: Proj3           /home/user/Science/Projects/AE/Proj3
Enter: Quit
?>
```
You then have to enter the index (number) corresponding to the project or toolbox you want to activate or deactivate. When you are done, simply press `Return` to exit the CLI.

### Import the project module in your programs

```
import project
```

In your programs, importing the `project` module gives you access to the current project path (`project.root`) and places all the packages and modules of the project automatically in your namespace.
