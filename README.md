# ProjectManager for Python

ProjectManager is a Python3 module easing the management of a collection of scientific projects and toolboxes.

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
alias projects='python3 /path/to/ProjectManager/project.py'
```

4) Restart your terminal.

5) Define where the projects and toolboxes are located by modifying the LOCATIONS file:
```
## Toolboxes
/home/user/Science/Toolboxes

## Projects
/home/user/Science/Projects
```

There can be multiple locations (one per line) in each section. In these directories, only the folders containing the `Peograms/Python` architecture are  recognized as valid toolboxes and projects. The search is recursive though, so the actual project location can be nested in a subfolder structure.

## Usage


