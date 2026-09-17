# PDS Cheatsheet

Running reference for Python for Data Science HS26, extended week by week.

The shell part builds on the PDS Linux cheatsheet by E. Mathis, S. Broda and R. Christen (HSLU, v0.4, ILIAS → *Supporting Material*), reorganized and extended.

- [Shell (Linux)](#shell-linux)
- [Python tooling](#python-tooling)
- [Python language](#python-language)

---

## Shell (Linux)

### Navigation

| Command | Description |
|---|---|
| `pwd` | Show current directory |
| `cd` or `cd ~` | Go to home directory |
| `cd ..` | One level up |
| `cd ../..` | Two levels up |
| `cd -` | Back to the previous directory |
| `cd data/raw` | Go into `data/raw` |
| `ls` | List directory content |
| `ls -l` | Long format with permissions, size, date |
| `ls -a` | Include hidden files |
| `ls -la` | Long format including hidden files |
| `ls -lh` | Long format with readable sizes |
| `ls -l *.csv` | Only `.csv` files |

### Files and folders

| Command | Description |
|---|---|
| `touch notes.txt` | Create an empty file |
| `mkdir -p data/raw` | Create a directory, including missing parents |
| `cp a.txt b.txt` | Copy a file |
| `cp -r src/ backup/` | Copy a folder |
| `mv old.txt new.txt` | Move or rename |
| `rm file.txt` | Delete a file |
| `rm -r folder/` | Delete a folder with its content, no undo |
| `find . -name "*.py"` | Search by name below the current directory |
| `grep -n "import" *.py` | Search text in files, with line numbers |
| `cat file.txt` | Print a file |
| `head -n 10 data.csv` | First 10 lines |
| `tail -n 10 data.csv` | Last 10 lines |
| `less file.txt` | Scroll through a file, `q` quits |
| `vim file.txt` | Edit in vim: `i` insert, `Esc` then `:wq` save and quit, `:q!` quit without saving |
| `curl -O https://example.com/data.csv` | Download a file (without `-O`, curl prints to the terminal) |
| `wget https://example.com/data.csv` | Download a file |

### Permissions and execution

| Command | Description |
|---|---|
| `chmod u+x run.sh` | Make executable for the owner |
| `chmod 644 file.txt` | Owner read and write, others read |
| `chmod 755 run.sh` | Owner everything, others read and execute |
| `./run.sh` | Run an executable in the current directory |

### Processes and system

| Command | Description |
|---|---|
| `ps aux` | Snapshot of all processes |
| `top` | Live process view, `q` quits |
| `kill 1234` | End the process with PID 1234 |
| `pkill jupyter` | End processes by name |
| `which python3` | Path of the binary that runs |
| `whereis python3` | Locations of binary, source and man page |
| `man ls` | Manual page |
| `uname -a` | Kernel and system information |
| `hostnamectl` | Machine information |
| `passwd` | Change your own password |
| `sudo passwd alice` | Change another user's password |
| `sudo reboot` | Reboot immediately |
| `sudo some-command` | Run as root |
| `!!` | Repeat the last command, `sudo !!` repeats it as root |
| `history` | Command history |
| `exit` | Close the terminal or SSH session |

| Key | Action |
|---|---|
| `Tab` | Autocomplete |
| `Ctrl+C` | Stop the running command |
| `Ctrl+R` | Search the history |
| `Ctrl+L` | Clear the screen |

### Packages (Debian / Ubuntu)

| Command | Description |
|---|---|
| `apt search htop` | Search packages |
| `apt-cache search htop` | Same, older tool, marks installed packages |
| `sudo apt update` | Refresh package lists |
| `sudo apt upgrade` | Upgrade all installed packages |
| `sudo apt install htop` | Install a package |
| `sudo apt install --only-upgrade htop` | Upgrade a single package |

`apt-get` accepts the same subcommands (`update`, `upgrade`, `install`).

### Network

| Command | Description |
|---|---|
| `ssh alice@server.example.com` | Open an SSH session |
| `scp alice@server.example.com:data.csv ./data/` | Download a file |
| `scp -r ./project alice@server.example.com:~/project` | Upload a folder |
| `ping -c 4 hslu.ch` | Send 4 pings |

### Troubleshooting

| Command | Description |
|---|---|
| `rm ~/.local/share/keyrings/login.keyring` | Reset the login keyring, all stored keys are lost |

---

## Python tooling

### Interpreter

| Command | Description |
|---|---|
| `python3 --version` | Interpreter version (short: `python3 -V`) |
| `python3` | Start the interactive console. Leave with `exit()` |
| `python3 script.py` | Run a script |
| `python3 -i script.py` | Run a script, then stay in the console with its variables |

Linux uses `python3`. On Windows the command is `python` or `py`.

### Virtual environment

| Task | Linux / macOS | Windows PowerShell |
|---|---|---|
| Create | `python3 -m venv .venv` | `python -m venv .venv` |
| Activate | `source .venv/bin/activate` | `.venv\Scripts\Activate.ps1` |
| Deactivate | `deactivate` | `deactivate` |

`. activate` and `source activate` from the course sheet are the same command and only work from inside `.venv/bin`. If PowerShell blocks the script: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### pip

| Command | Description |
|---|---|
| `pip list` | Installed packages |
| `pip install numpy` | Install a package |
| `pip install numpy==2.1.0` | Install a specific version |
| `pip install -U numpy` | Upgrade a package |
| `pip uninstall numpy` | Remove a package |
| `pip show numpy` | Version, location and dependencies |
| `pip freeze > requirements.txt` | Write the current environment to a file |
| `pip install -r requirements.txt` | Install everything from a file |
| `python -m pip install numpy` | Same as `pip install`, always uses the pip of this interpreter |

`pip search` no longer works because PyPI disabled its search API. Search on [pypi.org](https://pypi.org) or use the third-party tool `pip_search` (`pip install pip-search`).

### Jupyter

| Command | Description |
|---|---|
| `jupyter notebook` | Start a notebook server, opens the browser |
| `jupyter lab` | Start JupyterLab (needs the `jupyterlab` package) |
| `jupyter notebook list` | List running servers (classic Notebook) |
| `jupyter notebook stop 8888` | Stop the server on port 8888 (classic Notebook) |
| `jupyter server list` | List running servers (Notebook 7 and JupyterLab) |
| `jupyter server stop 8888` | Stop the server on port 8888 (Notebook 7 and JupyterLab) |
| `pkill jupyter` | Kill all Jupyter processes |

`jupyter-notebook` with a hyphen, as on the course sheet, is the same command.

### PyCharm shortcuts (Windows / Linux keymap)

| Shortcut | Action |
|---|---|
| `Ctrl+Shift+F10` | Run the current file |
| `Shift+F10` | Run the selected configuration |
| `Shift+F9` | Debug the selected configuration |
| `Ctrl+/` | Toggle comment |
| `Ctrl+Alt+L` | Reformat code |
| `Alt+Enter` | Quick fix |
| `Shift` twice | Search everywhere |

---

## Python language

### SW01 · Basics

#### Types

```python
42             # int, arbitrary precision
3.14           # float
5 + 3j         # complex
"text"         # str, 'text' is the same
True           # bool, subclass of int
None           # NoneType
[1, "a", 3]    # list: mutable, ordered
(1, "a", 3)    # tuple: immutable, ordered. One element: (1,)
{"a": 1}       # dict: key-value pairs, keys unique and hashable
{1, "a", 3}    # set: unique elements, unordered. Empty set: set()
```

#### Built-ins

| Function | Purpose |
|---|---|
| `print(a, b, sep=", ", end="\n")` | Output |
| `type(x)` | Type of an object |
| `isinstance(x, int)` | Type check, includes subclasses |
| `id(x)` | Identity of an object |
| `len(x)` | Length of a sequence or collection |
| `help(x)`, `dir(x)` | Documentation, list of attributes |
| `int()`, `float()`, `str()`, `bool()` | Convert scalars |
| `list()`, `tuple()`, `set()`, `dict()` | Convert collections |
| `abs(x)`, `round(x, n)`, `divmod(a, b)` | Number helpers |

#### Operators

| Operator | Meaning | Example |
|---|---|---|
| `+` `-` `*` | Add, subtract, multiply | `9 * 4` → `36` |
| `/` | Division, always float | `9 / 4` → `2.25` |
| `//` | Floor division | `9 // 4` → `2`, `-9 // 4` → `-3` |
| `%` | Remainder | `9 % 4` → `1`, `-9 % 4` → `3` |
| `**` | Power | `9 ** 4` → `6561` |
| `+` on sequences | Concatenate, same type only | `[1, 2] + [3]` → `[1, 2, 3]` |
| `*` on sequences | Repeat, int only | `"ab" * 3` → `"ababab"` |
| `==` `!=` `<` `<=` `>` `>=` | Comparison | `3 <= 4` → `True` |
| `and` `or` `not` | Logical | `True and not False` → `True` |
| `^` | Xor, bitwise but works on bools | `True ^ False` → `True` |

Precedence from high to low:
`**` → unary `-` → `* / // %` → `+ -` → `^` → comparisons → `not` → `and` → `or`

#### Pitfalls

| Expression | Result | Why |
|---|---|---|
| `0.1 + 0.2 == 0.3` | `False` | Binary floats. Use `math.isclose()` |
| `type({})` | `dict` | Empty set is `set()` |
| `type((1))` | `int` | Tuple needs a comma: `(1,)` |
| `-2 ** 2` | `-4` | `**` binds tighter than unary minus |
| `False and True == False` | `False` | Comparison runs first. Use parentheses |
| `round(2.5)` | `2` | Rounds half to even |
| `int(-3.9)` | `-3` | Truncates toward zero, `//` rounds down |
| `[[0] * 3] * 3` | 3 × the same list | Inner list is shared |
| `list = [1, 2]` | Works | Hides the built-in `list()` |

#### Naming

- Letters, digits and `_`, no digit at the start, case-sensitive, no keywords
- `snake_case` for variables and functions, `PascalCase` for classes, `UPPER_CASE` for constants