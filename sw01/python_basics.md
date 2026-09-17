# SW01 · Python Basics

**Date:** 2026-09-17, onsite
**Goals:** PyCharm installed and running, first Python exercises done

Topics: interpreter vs. compiler languages, IDE and PyCharm, console vs. script, virtual environments, variables, basic data types, operators.

---

## 1. Interpreter vs. compiler languages

|                     | Interpreter (script) language                     | Compiler language                                       |
| ------------------- | ------------------------------------------------- | ------------------------------------------------------- |
| Examples            | Bash, JavaScript, MATLAB, Python, R, Ruby         | C, C++, C#, Java                                        |
| Execution           | Interpreter runs the code directly, no build step | Compiler translates the source into an executable first |
| Interactive console | Yes, for ad-hoc commands                          | No                                                      |
| Optimization        | Little                                            | Compiler optimizes the code                             |
| Speed               | Slower                                            | Faster                                                  |
| Reverse engineering | Source is usually shipped as is                   | Harder, the executable is not human-readable            |

Python is an interpreter language. The Python console is the direct connection to the interpreter. A script is a collection of commands that are sent to the interpreter one after another.

> [!NOTE]
> **More precisely:** CPython does not execute the source text line by line. It first compiles the whole file to bytecode and then interprets that bytecode (imported modules are cached as `.pyc` files in `__pycache__/`). This is why a syntax error anywhere in a script stops it before the first line runs. A runtime error such as `NameError` only stops the script when that line is reached.
>
> Java and C# also compile to bytecode for a virtual machine (JVM, .NET CLR) and decompile quite well. The "hard to reverse-engineer" point really applies to native code from C and C++.

```python
# broken.py
x = 1
print(x)
print(y
```

```
$ python broken.py
  File "broken.py", line 3
    print(y
         ^
SyntaxError: '(' was never closed
```

`1` is never printed.

---

## 2. IDE and PyCharm

An Integrated Development Environment bundles the tools around the editor: debugger, terminal, file browser, version control, run configurations, remote development and execution, spell checker, TODO list. Any text editor works as well, the IDE only makes it more convenient.

### Setup

1. Install PyCharm from [jetbrains.com](https://www.jetbrains.com/pycharm/). On Linux: `sudo snap install pycharm-professional --classic`
2. Apply for the [JetBrains Student Pack](https://www.jetbrains.com/academy/student-pack/) with the `@stud.hslu.ch` address
3. Activate the licence in PyCharm under **Manage Subscriptions**
4. **New Project**: set name and location, interpreter type **Project venv** (creates the virtual environment in the project root)

### Layout

| Area      | Content                                          |
| --------- | ------------------------------------------------ |
| Left      | Project tree                                     |
| Center    | Editor with file tabs                            |
| Top right | Run and debug controls                           |
| Bottom    | Tool windows: Run, Python Console, Terminal, Git |

### First command

Open the Terminal tool window, start `python` and enter:

```python
print("hello world")
```

The Python Console tool window gives the same interactive console without the terminal step.

---

## 3. Console vs. script

**Console (REPL):** every statement goes to the interpreter and the result appears on the next line. Expressions are echoed automatically, no `print` needed.

```python
>>> 3 + 4
7
>>> _ * 2        # _ holds the last result
14
```

**Script:** a `.py` file. Running it sends all statements to the interpreter in order. Only `print` produces output.

```python
# hello_world.py
print('hello world')
print('-' * 3)
a = 3
b = 5 - a
print('hello world\n' * b)
```

```
hello world
---
hello world
hello world

```

The empty last line comes from the `\n` inside the string plus the newline `print` adds.

Run a script with `python hello_world.py` (Linux: `python3`) or in PyCharm with the run button or `Ctrl+Shift+F10`. `python -i hello_world.py` runs the script and then keeps the console open with its variables.

### Comments

```python
# a comment runs until the end of the line
x = 3  # also after code
```

---

## 4. Virtual environments

Python ships with built-in functions such as `print()`, `abs()`, `str()` and `open()`. Most applications also need external packages, installed with pip (Package Installer for Python) from PyPI.

A virtual environment (venv) gives each project its own set of packages. This avoids version conflicts between projects and keeps the system Python clean.

```
Operating system (Linux, macOS, Windows)
└── System Python with a few packages
    └── Project venv with project-specific packages
```

| Task                        | Linux / macOS               | Windows PowerShell           |
| --------------------------- | --------------------------- | ---------------------------- |
| Create                      | `python3 -m venv .venv`     | `python -m venv .venv`       |
| Activate                    | `source .venv/bin/activate` | `.venv\Scripts\Activate.ps1` |
| Deactivate                  | `deactivate`                | `deactivate`                 |
| Which interpreter is active | `which python`              | `Get-Command python`         |
| Install a package           | `pip install numpy`         | `pip install numpy`          |
| List packages               | `pip list`                  | `pip list`                   |

`python -m pip install numpy` does the same as `pip install numpy` but guarantees that the pip of the current interpreter is used.

> [!WARNING]
> The slide writes `Python3 –m venv venvName`. Copied as is, this fails. On Linux the command is lowercase `python3`, and the flag is `-m` with a plain hyphen, not an en dash.

---

## 5. Variables

The slide describes a variable as name, data type, storage location and value. Unlike C, C# or Java, Python needs no type declaration. The type comes from the value.

```python
x = 99           # Python: name = value
```

In C, C# or Java the type is declared: `int x = 99`

> [!NOTE]
> **More precisely:** a Python variable is a name bound to an object. The object carries type, value and memory location, the name does not. The same name can later point to an object of another type, and two names can point to the same object.

```python
x = 99
type(x)          # <class 'int'>
x = "text"
type(x)          # <class 'str'>

a = [1, 2]
b = a            # b is a second name for the same list
b.append(3)
a                # [1, 2, 3]
```

The second example comes back in SW10 (shallow vs. deep copy).

### Naming rules

- Letters, digits and underscore. No digit at the start. A leading underscore is allowed and by convention marks internal names.
- Case-sensitive: `data` and `Data` are different names.
- Keywords such as `class`, `for` or `lambda` are not allowed. Full list: `import keyword` then `keyword.kwlist`
- Do not reuse built-in names like `list`, `dict`, `str` or `sum`. It works, but the built-in is no longer reachable under that name.

### Conventions (PEP 8)

| Kind                 | Style        | Example       |
| -------------------- | ------------ | ------------- |
| Variables, functions | `snake_case` | `hello_world` |
| Classes              | `PascalCase` | `DataLoader`  |
| Constants            | `UPPER_CASE` | `MAX_ITER`    |

> [!NOTE]
> The slide says camelCase is "not really used (allowed)". It is allowed, `helloWorld = 1` runs fine. It only goes against the PEP 8 convention.

---

## 6. Basic data types

### Scalar types

| Type       | Example                                    | Notes                                                |
| ---------- | ------------------------------------------ | ---------------------------------------------------- |
| `int`      | `42`, `-7`, `2 ** 100`                     | Arbitrary precision, no overflow                     |
| `float`    | `3.1415`, `1e-3`                           | Binary floating point, `0.1 + 0.2 == 0.3` is `False` |
| `complex`  | `5 + 3j`                                   | `.real` and `.imag` return floats                    |
| `str`      | `"hello 'my' world"`, `'hello "my" world'` | Immutable. Single and double quotes are equivalent   |
| `bool`     | `True`, `False`                            | Subclass of `int`, `True + True` is `2`              |
| `NoneType` | `None`                                     | Absence of a value                                   |

### Collection types

| Type    | Literal                  | Mutable | Ordered         | Duplicates  | Notes                                       |
| ------- | ------------------------ | ------- | --------------- | ----------- | ------------------------------------------- |
| `list`  | `[1, "hello", 3]`        | yes     | yes             | yes         | Mixed types allowed                         |
| `tuple` | `(1, "hello", 3)`        | no      | yes             | yes         | One element needs a comma: `(1,)`           |
| `dict`  | `{"a": 1, "b": "hello"}` | yes     | insertion order | keys unique | Keys must be hashable (no lists)            |
| `set`   | `{1, "hello", 3}`        | yes     | no              | no          | `{}` is an empty dict, empty set is `set()` |

### Type check and conversion

```python
type(3.0)            # <class 'float'>
isinstance(3, int)   # True
int("42")            # 42
int(3.9)             # 3, truncates toward zero
int(-3.9)            # -3
float("3.14")        # 3.14
str(42)              # '42'
bool("")             # False, empty values are falsy
bool("False")        # True, any non-empty string is truthy
round(2.5)           # 2, rounds half to even
```

---

## 7. Arithmetic operators

| Operator | Meaning                          | Example           |
| -------- | -------------------------------- | ----------------- |
| `x + y`  | addition                         | `9 + 4` → `13`    |
| `x - y`  | subtraction                      | `9 - 4` → `5`     |
| `x * y`  | multiplication                   | `9 * 4` → `36`    |
| `x / y`  | division, always returns a float | `9 / 4` → `2.25`  |
| `x // y` | floor division                   | `9 // 4` → `2`    |
| `x % y`  | remainder (modulo)               | `9 % 4` → `1`     |
| `x ** y` | power                            | `9 ** 4` → `6561` |

Details worth knowing:

```python
8 / 4          # 2.0, not 2
-9 // 4        # -3, rounds down, not toward zero
-9 % 4         # 3, sign follows the divisor
divmod(9, 4)   # (2, 1)
3 + 2.0        # 5.0, int and float give float
0.1 + 0.2      # 0.30000000000000004
```

Precedence from high to low: `**`, unary `-`, `* / // %`, `+ -`

```python
3 + 4 * 2 ** 2   # 19
-2 ** 2          # -4, same as -(2 ** 2)
(-2) ** 2        # 4
2 ** 3 ** 2      # 512, ** evaluates right to left
```

---

## 8. `+` and `*` on sequences

For strings, lists and tuples, `+` concatenates. Both sides must have the same type.

```python
'hello' + ' ' + 'world'    # 'hello world'
[1, 2, 3] + [4, 5]         # [1, 2, 3, 4, 5]
'a' + 1                    # TypeError: can only concatenate str (not "int") to str
'a' + str(1)               # 'a1'
```

`*` repeats a sequence and needs an integer.

```python
'hello|' * 3               # 'hello|hello|hello|'
[1, 2, 3] * 3              # [1, 2, 3, 1, 2, 3, 1, 2, 3]
'ab' * 0                   # ''
[1, 2] * 2.0               # TypeError: can't multiply sequence by non-int of type 'float'
'hello|' * 3 + 'hello'     # 'hello|hello|hello|hello', * runs before +
```

> [!WARNING]
> `[[0] * 3] * 3` creates three references to the same inner list. Changing one row changes all three. More on this in SW10.

---

## 9. Boolean operators

| `a`     | `b`     | `a and b` | `a or b` | `a ^ b` (xor) |
| ------- | ------- | --------- | -------- | ------------- |
| `True`  | `True`  | `True`    | `True`   | `False`       |
| `True`  | `False` | `False`   | `True`   | `True`        |
| `False` | `True`  | `False`   | `True`   | `True`        |
| `False` | `False` | `False`   | `False`  | `False`       |

`not` inverts a value: `not True` is `False`. `a != b` is the common way to write a logical xor.

Precedence from high to low: `^`, comparisons (`==`, `<`, ...), `not`, `and`, `or`

> [!WARNING]
> The slide writes statements like `True and False == False`. As Python code this parses as `True and (False == False)`, not as `(True and False) == False`. Often the result happens to match, but not always:

```python
False and True == False      # False, evaluated as False and (True == False)
(False and True) == False    # True
```

Use parentheses when mixing boolean and comparison operators.

`and` and `or` stop as soon as the result is known and return one of the operands, not necessarily a bool:

```python
0 or "default"     # 'default'
"a" and "b"        # 'b'
```

---

## 10. Exercises and reading

### This week

- [ ] Install PyCharm and activate the student licence
- [ ] Create a new project with a Project venv interpreter
- [ ] Run `print("hello world")` in the Python console
- [ ] Write a script with variable assignments, basic math operations and `print` calls
- [ ] ILIAS ad-hoc exercises (PDS course container, section _Exercises_)

### Reading

- Course book: data types, variables, comments
- tutorials.eu, _The Complete Python 3 Masterclass_: section 2 (Python basics), section 3 (Python basics part 2), section 4 (control structures)
