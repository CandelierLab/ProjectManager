# ProjectManager for Python

ProjectManager is a Python module easing the management of a collection of scientific projects and toolboxes.

Projects and toolboxes are simply directories with whatever architecture, the only constraint being that it must contain a `Programs/Python` folder/subfolder. For instance, a valid project could be:

```
project
  ├── Programs
  │   ├── Python      ☚ Mandatory structure stops here, the rest is optional
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



## Setup

1) Permanently add the project module in the PYTHONPATH. Add the following line at the end of ~/.bashrc:

export PYTHONPATH=$PYTHONPATH:/home/raphael/Science/Tools/Projects

2) Add an alias for launching the project module. In ~/.bash_aliases, add:

alias projects='python3 /home/raphael/Science/Tools/Projects/project.py'

3) Restart your terminal.

4) Define the projects' folders in the LIST file, with one line per folder path

## Usage