# SW08 · Modules and Packages

**Date:** 2026-11-05, onsite
**Slides:** `sw08_packaging.pdf` (dated 11 Nov 2026) · **Exercises:** [SW08 exercise sheet](sw08_exercises.md)

Topics: modules, import forms, absolute and relative paths, `if __name__ == "__main__"`, namespace and scope, docstrings, packaging and `__init__.py`, pip and external packages.

The slide deck's page footers are unreliable this week. Several section dividers carry stale numbers, so "Page 4", "Page 5" and "Page 10" each appear on two different slides. Go by section, not by page.

## Contents

1. [Concept](#1-concept)
2. [Import forms](#2-import-forms)
3. [A module is executed on import](#3-a-module-is-executed-on-import)
4. [Absolute and relative paths](#4-absolute-and-relative-paths)
5. [Extending the search path](#5-extending-the-search-path)
6. [Multiple imports and the asterisk](#6-multiple-imports-and-the-asterisk)
7. [if __name__ == "__main__"](#7-if-__name__--__main__)
8. [Namespace and scope](#8-namespace-and-scope)
9. [Documentation with docstrings](#9-documentation-with-docstrings)
10. [Packaging](#10-packaging)
11. [External packages and pip](#11-external-packages-and-pip)

---

## 1. Concept

> "A module is a file containing Python definitions and statements."

Modules structure the source code of the whole application, which allows for:

1. having code more organised and easier maintenance
2. developing libraries that can be used in different applications

A module can contain definitions like variables or Enums, functions, classes, structs and so on. The slide's worked example is the standard library's own `stat.py`, which is exactly that: a docstring, a block of constants, then a set of functions.

The practical point of the `stat.py` example is that there is nothing special about library modules. A file you write and a file that ships with Python are the same kind of thing.

## 2. Import forms

To access the content of other modules, they can be imported as a whole or in parts.

1. **The name of a module is the file name without the extension** `.py`.
2. With reference to the module name, selected parts can be imported.

Given `hi.py`:

```python
hi_term = 'hello world'

def say_hi(name=hi_term):
    print(name)

class Welcome:
    def __init__(self, name):
        self.name = name

    def say_welcome(self):
        say_hi(self.name)
```

| Import | What it declares | Access |
|---|---|---|
| `import hi` | reference to module `hi.py` | `my_var = hi.hi_term` |
| `import hi as hi_mod` | renames the reference to `hi_mod` | `my_var = hi_mod.hi_term` |
| `from hi import Welcome` | reference to a specific attribute | `my_var = Welcome('Peter')` |
| `from hi import *` | references to "all" attributes | `my_var = say_hi()` |

Rule 1 is the one that bites in the [exercise](sw08_exercises.md#exercise-2-modules): if the file on disk is called `exercise_string_operations.py`, then `import string_operations` fails. The import name and the file name are the same string.

> **Try to import the module `antigravity.py`. What happens?**

It opens [xkcd 353](https://xkcd.com/353/) in your browser. It is a joke module in the standard library, and the point behind it is real: `import` runs code, so importing something is never a neutral act.

## 3. A module is executed on import

When you refer to a module to import all or any part of it, **the full module is interpreted**. The interpreter starts at the top of the referred module and goes through all of its content, executing every statement and declaration.

This holds for importing a whole module:

```python
import path.to.module
```

as well as for parts of it:

```python
from path.to.module import attribute
```

The slide's example: `main.py` does `from my_script import my_var`, and `my_script.py` contains a top-level `print(my_var)`. That `print` runs, even though only `my_var` was asked for.

This is the reason for [`if __name__ == "__main__"`](#7-if-__name__--__main__). Anything at module top level is a side effect of importing, so a module meant to be imported should define things at the top level and *do* things only under that guard.

A module is executed **once per process**. A second `import` of the same module reuses the cached object in `sys.modules` and does not re-run the file.

## 4. Absolute and relative paths

Referring to external modules and files requires either absolute or relative references.

- By default, **root is set to the main executed script**.
- The folder of the main script is not visible in the main script itself, nor at lower levels.

The slide's project tree:

```
a/
 | sa.py
 | saa.py
 |
 |-b/
    | sb.py
    | sbb.py
    |
    |-c/
       | sc.py
```

Assume running `sb.py`, so root is `b/`:

| Absolute path | Meaning |
|---|---|
| `import c.sc` | full module `sc.py` |
| `from c.sc import var` | import `var` of module `sc.py` |
| `import a.b.sc` | import beyond top level |

Assume `sb.py` is imported in `sa.py`, so root becomes `a/`:

| Relative path | Meaning |
|---|---|
| `import c.sc` | **not possible any more**, root is `a/` |
| `from .c import sc` | in `sb.py`: import module `sc.py` relative to `sb.py` |
| `from ..sb import var` | in `sc.py`: possible, as `b/` exists within the root dir |

**The rule that makes this usable in practice.** A relative import only works when the module was itself imported **as part of a package**. Run the same file directly and it fails:

```
$ python3 sub/user.py
ImportError: attempted relative import with no known parent package

$ python3 -c "import sub.user"
from helper
```

Same file, same `from .helper import value`, two different outcomes. The difference is whether Python knows a parent package, and running a file as `__main__` means it does not. If you hit that error, you ran a file that was meant to be imported.

Docs: [importing from a package](https://docs.python.org/3/tutorial/modules.html#importing-from-a-package)

## 5. Extending the search path

By default, imported modules are searched relative to the script path. Sometimes scripts live elsewhere, for example a collection of personal libraries, and the interpreter should also search there.

The `sys` module extends the search space:

```python
sys.path.append('C:\\Users\\additional\\location')     # Windows
sys.path.append('/home/username/additional/location')  # Linux
```

Use this sparingly. It makes the program depend on a machine-specific path, which breaks for everyone else. A package installed with `pip install -e .` solves the same problem without hard-coding anything.

## 6. Multiple imports and the asterisk

Python allows tweaks for importing attributes, including multiple imports on a single line and the asterisk operator:

```python
from b.b import var1, var2
from b.b import var1 as v1, var2 as v2
```

The asterisk imports all attributes by name, so `var1` and `var2` are accessible without a module reference:

```python
from b.b import *
```

However, for large modules this blows up the final sources unnecessarily.

**Slide correction.** The slide says that both chained imports and the asterisk operator "should not be used as by convention", citing PEP 8. That is only half right.

- **Wildcard imports are genuinely discouraged.** PEP 8 says they should be avoided, because they make it unclear which names are present in the namespace.
- **`from module import a, b` is explicitly allowed.** PEP 8's rule about separate lines applies to `import sys, os`, two *modules* on one `import` line. It then says in so many words that `from subprocess import Popen, PIPE` is fine.

So the thing to avoid is `import sys, os` and `from x import *`. Putting several names in one `from` import is normal Python.

[PEP 8](https://peps.python.org/pep-0008/)

## 7. `if __name__ == "__main__"`

When the interpreter declares a module, it assigns a unique name to it.

- The module name equals the path from root, dot separated, plus the file name without the `.py` appendix. The module name of `my_mod.py` is `path.to.module.my_mod`.
- **The module name of the first interpreted module, the main module, is set to `__main__`.**

So the two cases can be distinguished programmatically:

```python
from s.th import attr

some_var = 'hello world'

if __name__ == '__main__':
    print(f"{some_var=}")
```

Verified:

```python
>>> __name__                 # in the script you ran
'__main__'
>>> string_operations.__name__   # in a module you imported
'string_operations'
```

If you write a module intended to be used **both** as a standalone script and as a code source to be imported, use this pattern. Typical use cases:

- testing parts of code
- running modules with default settings

## 8. Namespace and scope

A **namespace** defines the visibility of a unique name for every object, variable or method. Python has three:

| Namespace | Contains | Lifetime ends |
|---|---|---|
| **built-in** | no programmer-defined objects | when the application ends |
| **global** | programmer-defined objects available across the whole script | when the module is unloaded or the application ends |
| **local** | programmer-defined objects in function blocks | when the function block has finished |

```
┌─ built-in namespace ──────────────────────────┐
│  ┌─ global namespace ───────────────────────┐ │
│  │   ┌─ local namespace ─┐                  │ │
│  │   └───────────────────┘                  │ │
│  │   ┌─ local namespace ─┐                  │ │
│  │   └───────────────────┘                  │ │
│  └──────────────────────────────────────────┘ │
└───────────────────────────────────────────────┘
```

- Object names must only be unique **within** a given namespace. The global namespace can therefore have multiple local namespaces holding objects with the same name.
- The **scope** of an object is the code section from which it is accessible.

Note "global" means module-level, not program-wide. Each module has its own global namespace, which is why `import` gives you `hi.hi_term` rather than a bare `hi_term`.

### What if a function (a) returns a reference to another function (b)?

```python
def my_fun():
    def num_sum(a, b):
        return a + b
    return num_sum

print(my_fun()(1, 2))    # 3
```

- a scope returns a new scope
- the lifetime of the scope of function (a) ends with the return of the scope (b)
- the scope of function (b) is created when (b) is called and ends when it reaches the end of its block

`my_fun()` returns the function object itself, not a call to it, which is why the result is called immediately with `(1, 2)`. This is the same "functions can return references to any data type, including other functions" point from [SW05](../sw05/sw05_functions_files.md#7-return-values).

## 9. Documentation with docstrings

Python offers centralised documentation with **docstrings**, a built-in attribute assigned to each function, named `__doc__`:

```python
definition.__doc__
```

> ...comprises the documentation string of a class or function, or `None` if undefined.

Docstrings can document a **package** (in `__init__.py`), a **class**, a **module** and a **function**.

If `__doc__` is set, it is callable by means of `help(...)`:

```python
>>> help(fun)
```

Docstrings can be set to any custom object, except built-ins and extensions of type `str`, in two ways:

1. **explicitly**, by writing to the attribute: `fun.__doc__ = "Sample function for ..."`
2. **implicitly**, by placing a triple-quoted string block immediately next to the definition

Conventions are given in [PEP 257](https://peps.python.org/pep-0257/).

One detail that shows up in the [exercise](sw08_exercises.md#exercise-2-modules): a docstring written as

```python
'''
Collection of methods to manipulate strings.
'''
```

keeps the newlines, so `__doc__` is `'\nCollection of methods to manipulate strings.\n'` and printing it produces a blank line before and after the text.

## 10. Packaging

### Folder versus package

Python considers a regular system folder a simple structural element that can contain modules (`.py`) or resource files such as data files (`.json`, `.csv`), text (`.txt`), figures (`.jpg`, `.png`) or icons (`.ico`).

Modules and objects can be imported from folders using the dot notation:

```python
from path.to.folder import module
```

**A folder becomes a package as soon as it contains a script named `__init__.py`.**

```python
from path.to.package import module
```

Contrasting with folders, a package can also be imported like a regular module. The `__init__.py` script is invoked when the package, a module from it, or any object of it is imported. The exception is namespace packages.

### The `__init__.py` script

Like a module that gets imported, `__init__.py` is interpreted when the package or parts of it get imported. It can:

- be empty
- import additional modules
- define variables, functions, classes and so on
- be used to keep an interface of a module when it is turned into a package

Objects defined in `__init__.py` are bound to names in the package's namespace, and **the `__name__` of `__init__.py` is the package name**.

Verified:

```
$ python3 -c "from sub.helper import value; print(value)"
__init__ of sub ran, __name__ = sub
from helper
```

Importing one module out of the package still ran the package's `__init__.py` first, and its `__name__` is `sub`, not `sub.__init__`.

Docs: [regular packages](https://docs.python.org/3/reference/import.html#regular-packages)

### Deployment

Python is a script language, so distributing packages requires no special compilation or packing. Sharing library functions or modules with colleagues can be done by exchanging Python modules, packages or directories.

Following some additional deployment constraints, packages can also be provided to:

1. the official Python Package repository, **PyPI**
2. the **Test PyPI** repository

Docs: [packaging projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

## 11. External packages and pip

The Python Software Foundation hosts its own repository for official Python packages, called **PyPI** ([pypi.org](https://pypi.org)).

**pip** is a command-line tool for installing Python packages, included with modern versions of Python.

| Command | Does |
|---|---|
| `install` | install packages |
| `download` | download packages |
| `uninstall` | uninstall packages |
| `freeze` | output installed packages in requirements format |
| `list` | list installed packages |
| `show` | show information about installed packages |
| `help` | show help for commands |

Packages can be installed from `.zip` packages, version control systems such as Git or Bitbucket, and PyPI.

To install from the official repository:

1. look for the desired package on pypi.org
2. open a CLI and make sure pip is installed
3. run `pip install <package_name>`

Changing the URL targets a different repository:

```bash
pip install git+https://github.com/user/repo.git@develop
```

`pip freeze > requirements.txt` is the one worth remembering, since it is how this repo's own [`requirements.txt`](../requirements.txt) is kept current. Always install into the activated virtual environment, otherwise the package lands in the system Python and the venv still cannot see it.
