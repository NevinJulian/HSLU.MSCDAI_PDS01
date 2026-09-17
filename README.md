# Python for Data Science (PDS) · HS26

Notes, exercises and a running cheatsheet for the module **Python for Data Science** in the MSc Applied Information and Data Science at HSLU, autumn semester 2026.

## Module

| | |
|---|---|
| Module | Python for Data Science (PDS) |
| Code | W.MSCIDS_PDS01.H26 |
| Semester | HS26, 17 Sep to 17 Dec 2026 |
| Lecturers | Andreas Melillo, Ramón Christen |
| Research associate | Tim Giger |
| Format | Theory with live coding, then exercises. Onsite sessions are streamed passively (except SW13). |
| Course book | Bernd Klein, *Einführung in Python 3*, 4th ed., Hanser, ISBN 978-3-446-46379-0 |

## Semester plan

| SW | Date | Mode | Topic | Content | Notes |
|---|---|---|---|---|---|
| 01 | 2026-09-17 | onsite | Python Basics | Script vs. compiled languages, PyCharm setup, console vs. script, data types and operations | [SW01](sw01/sw01_python_basics.md) |
| 02 | 2026-09-24 | online | Control Structures I | Slicing, if-else, short-hands, match-case | |
| 03 | 2026-10-01 | online | Control Structures II | while and for loops, AI | |
| 04 | 2026-10-08 | onsite | Files, Functions I, Strings | Reading and writing files, function basics, strings, string formatting | |
| 05 | 2026-10-15 | online | Namespaces, Functions II | Parameter properties, (un)packing, recursion | |
| 06 | 2026-10-22 | online | OOP I | Classes: attributes, constructor, methods, properties | |
| 07 | 2026-10-29 | onsite | OOP II | Class vs. instance attributes, inheritance, multiple inheritance | |
| 08 | 2026-11-05 | onsite | Modules | Modules, packages, imports, namespaces, remote development | |
| 09 | 2026-11-12 | online | External Packages | pandas, NumPy, data visualization, Jupyter and marimo notebooks | |
| 10 | 2026-11-19 | online | Short Expressions | Shallow vs. deep copy, lambda functions, list comprehensions, type annotations | |
| 11 | 2026-11-26 | onsite | Hackathon | Collaborative exercise | |
| 12 | 2026-12-03 | online | Special Iterators, Exceptions | Generators, iterators, try-except | |
| 13 | 2026-12-10 | onsite | Exam Preparation | Exercise set, mock exam, no streaming | |
| 14 | 2026-12-17 | online | Wrap-up | Exercise discussion, final Q&A | |

Source: semester plan V1.0 from 11 Sep 2026. Changes are published on ILIAS.

## Repository structure

```
.
├── README.md
├── cheatsheet.md              running reference, extended every week
├── sw01/
│   ├── sw01_python_basics.md  lecture notes
│   └── *.py                   exercise scripts
├── sw02/
└── ...
```

Every week gets its own folder `swXX/` with a notes file and the exercise code of that week. The [cheatsheet](cheatsheet.md) collects shell commands, tooling and language basics in one place.

## Setup

Requirements: Python 3 and PyCharm. The PyCharm licence comes with the [JetBrains Student Pack](https://www.jetbrains.com/academy/student-pack/) (register with the `@stud.hslu.ch` address).

Create and activate the virtual environment from the repository root:

```bash
# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

```powershell
# Windows PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell refuses to run the activation script, allow local scripts once with `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

In PyCharm, select the environment under **Settings → Project → Python Interpreter → `.venv`**.

External packages start in SW09. From then on, dependencies are tracked in `requirements.txt`:

```bash
pip install -r requirements.txt   # install all dependencies
pip freeze > requirements.txt     # update after adding a package
```

`.venv/`, `.idea/` and `__pycache__/` belong in `.gitignore`.

## Resources

- [Python documentation](https://docs.python.org/3/)
- Course book online: [python-course.eu](https://www.python-course.eu/) (EN), [python-kurs.eu](https://www.python-kurs.eu/) (DE), [PDF tutorial](https://www.python-course.eu/bernd_klein_python_tutorial_a4.pdf)
- [Python Beginner's Guide](https://wiki.python.org/moin/BeginnersGuide)
- [PEP 8 style guide](https://peps.python.org/pep-0008/)
- ILIAS, PDS course container: weekly ad-hoc exercises (section *Exercises*), Linux cheatsheet (section *Supporting Material*), link to the tutorials.eu online course