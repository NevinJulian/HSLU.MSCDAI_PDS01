# SW08 · Exercise sheet: simple numpy, modules

**Sheet:** `exercises.pdf` ("Exercise Sheet SW8") · **Theory:** [SW08 notes](sw08_modules.md)
**Code:** [exercise/sw08_exercises.ipynb](exercise/sw08_exercises.ipynb) · [exercise/run_script.py](exercise/run_script.py) · [exercise/string_operations.py](exercise/string_operations.py)

Additional material: download `exercise_run_script.py` and `exercise_string_operations.py` from ILIAS. Both are in [`exercise/`](exercise/) with the `...FILL HERE...` placeholders intact, under the names the import statements need (see [Exercise 2](#exercise-2-modules)).

Both solutions were run on Python 3.13 with numpy 2.5.3. Solutions are collapsed, try the task first.

---

## Exercise 1: simple numpy

Path to your first external package functionalities:

- Install Numpy on your environment
- Import the external source, that is, the Numpy package
- Copy the list of float numbers from below
- Use the Numpy package to compute the 50% and 95% percentile

```python
list_of_numbers = [0.029, 0.551, 0.27, 0.727, 0.867, 0.954, 0.360, 0.018, 0.045, 0.470,
 0.455, 0.628, 0.538, 0.524, 0.449]
```

<details>
<summary>Solution</summary>

**Install.** With the repo's virtual environment activated:

```bash
pip install numpy
```

Check it landed in the venv and not in the system Python:

```bash
pip show numpy
```

Then record it in the project's dependency list, which is what [`requirements.txt`](../requirements.txt) is for:

```bash
pip freeze > requirements.txt
```

**Compute.**

```python
import numpy as np

list_of_numbers = [0.029, 0.551, 0.27, 0.727, 0.867, 0.954, 0.360, 0.018, 0.045, 0.470,
 0.455, 0.628, 0.538, 0.524, 0.449]

print(np.percentile(list_of_numbers, 50))
print(np.percentile(list_of_numbers, 95))
```

```
0.47
0.8930999999999999
```

**What a percentile is.** The value below which that share of the data falls. The 50th percentile is the median, so `np.percentile(x, 50)` and `np.median(x)` return the same number. With 15 values the median is simply the 8th of the sorted list:

```
[0.018, 0.029, 0.045, 0.27, 0.36, 0.449, 0.455, 0.47, 0.524, 0.538, 0.551, 0.628, 0.727, 0.867, 0.954]
                                              ↑ index 7, the 8th value
```

**Why 95% is not one of your numbers.** The 95% position is `0.95 × (15 − 1) = 13.3`, which falls between the 14th and 15th sorted values, 0.867 and 0.954. Numpy interpolates linearly:

```
0.867 + (0.954 − 0.867) × 0.3 = 0.8931
```

That interpolation is a default, not a law. `np.percentile(x, 95, method="lower")` returns 0.867, an actual data point. Worth knowing before you quote a percentile from someone else's code.

**Why the trailing `...999`.** `0.8930999999999999` is the usual binary floating point representation, the same effect as `0.1 + 0.2` in [week 1 of CSC](https://en.wikipedia.org/wiki/Floating-point_arithmetic). Round for display with `round(value, 4)` or an f-string, do not try to fix the value itself.

**The slide version uses different numbers.** The deck's last-but-one slide gives the same 15 values at full precision rather than rounded to three decimals, which yields 0.47025653079756413 and 0.8934795116813452. Either is fine, the sheet's list is the one to hand in.

**`import numpy as np` is the convention.** The `as` form from [the notes](sw08_modules.md#2-import-forms), with a name the whole ecosystem agrees on. Every numpy example you will read uses `np`, so do not invent an alias.

`np.percentile` takes the list directly, no `np.array(...)` needed. Converting first only pays off when you reuse the array several times.

</details>

## Exercise 2: modules

Complete the files such that the following code becomes executable and matches the given OUT-statements. All of the commands should be executed inside the file `exercise_run_script.py`.

**Hint:** you also need to make adjustments in the second file.

```python
print(SO.__doc__)
#OUT: Collection of methods to manipulate strings.

SO.say_something()
#OUT: Hello

print(SO.module_variable)
#OUT: Hello

print(rev)
#OUT: !esrevinU olleH

print(bi_rev)
#OUT: !seiUolH

# Import specific function from string_operation!
print(reverse("!esrevinU olleH"))
#OUT: Hello Universe!

# greet somebody in reversed order
name = 'Andreas'
print(greet_somebody(reverse(name)))
#OUT: Hello saerdnA
```

<details>
<summary>Solution</summary>

**First, sort out the file names.** ILIAS hands the files out as `exercise_run_script.py` and `exercise_string_operations.py`, and the sheet refers to them by those names. But the starter script already contains a hard-coded line:

```python
from string_operations import ...FILL HERE...
```

with the placeholder on the *function* name, not the module. The module name is the file name without `.py`, so that line only resolves against a file called `string_operations.py`. Two ways out:

1. **Rename the module file to `string_operations.py`.** This is what the slides call it, and it leaves the given import lines untouched. The copies in `exercise/` are already named this way.
2. Keep `exercise_string_operations.py` and change every import to match it.

Option 1 is the one to take. Only the module file matters, the driver script can keep any name you like since nothing imports it.

**string_operations.py**

```python
'''
Collection of methods to manipulate strings.
'''
module_variable = 'Hello'

def reverse(string):
    return string[::-1]

def bi_rev(string):
    return string[::-2]

def say_something():
    print(module_variable)

def greet_somebody(name):
    return f"Hello {name}"
```

**run_script.py**

```python
import string_operations as SO

print(SO.__doc__)

SO.say_something()

print(SO.module_variable)

my_string = 'Hello Universe!'
rev = SO.reverse(my_string)
print(rev)

bi_rev = SO.bi_rev(my_string)
print(bi_rev)

from string_operations import reverse
print(reverse("!esrevinU olleH"))

from string_operations import greet_somebody
name = 'Andreas'
print(greet_somebody(reverse(name)))
```

Actual output, every line matching its `#OUT:`:

```

Collection of methods to manipulate strings.

Hello
Hello
!esrevinU olleH
!seiUolH
Hello Universe!
Hello saerdnA
```

**How each blank is pinned down.** None is a free choice, every one is forced by an expected output:

| Blank | Value | Why |
|---|---|---|
| module name | `string_operations` | The file name, [rule 1 of importing](sw08_modules.md#2-import-forms) |
| docstring | `methods to manipulate strings.` | Printed verbatim by `print(SO.__doc__)` |
| `module_variable` | `'Hello'` | `print(SO.module_variable)` outputs `Hello` |
| the missing function | `say_something()`, printing `module_variable` | Called as `SO.say_something()`, outputs `Hello` |
| `my_string` | `'Hello Universe!'` | Its reverse is `!esrevinU olleH` |
| the second method | `bi_rev` | `'Hello Universe!'[::-2]` is `!seiUolH` |
| first `from` import | `reverse` | Used bare on the next line |
| second `from` import | `greet_somebody` | Used bare on the next line |
| `greet_somebody` body | `return f"Hello {name}"` | Wrapped in `print(...)`, so it returns rather than prints |

The sheet's listing leaves out the `import ... as SO` line and the `my_string = ...` line, since it only shows the output-producing statements. The starter file has the full skeleton, so work from that.

**Why `bi_rev` gives `!seiUolH`.** `[::-2]` walks backwards taking every second character. From index 14 down:

```
H  e  l  l  o     U  n  i  v  e  r  s  e  !
0  1  2  3  4  5  6  7  8  9 10 11 12 13 14
▲     ▲     ▲     ▲     ▲     ▲     ▲     ▲
```

**`print` versus `return`, again.** `say_something()` is called bare, so it prints. `greet_somebody()` is called inside `print(...)`, so it returns. Getting these the wrong way round gives `None` on screen or nothing at all. Same distinction as in [SW06](../sw06/sw06_exercises.md) and [SW07](../sw07/sw07_exercises.md).

**Two details in the finished script:**

- `print(SO.__doc__)` produces a **blank line before and after** the text, because the triple-quoted docstring starts and ends with a newline. The `#OUT:` comment shows only the text, so this is not a mistake in your solution.
- `bi_rev = SO.bi_rev(my_string)` gives the variable the same name as the function. It works here because the function is only reached through `SO.`, but had the script done `from string_operations import bi_rev` first, that line would have overwritten the function with a string. Avoid shadowing a name you still need.

**A thing to try.** Add `print("module loaded")` at the top of `string_operations.py` and run the script. It prints **once**, despite three separate import statements, because a module is executed once per process and later imports reuse the cached object. That is [section 3 of the notes](sw08_modules.md#3-a-module-is-executed-on-import) in one experiment.

</details>

---

## Notes for the exam

- The module name is the file name without `.py`. Rename the file and the import breaks.
- Importing a module **runs** it, top to bottom, once per process. Anything that should not run on import goes under `if __name__ == "__main__"`.
- `__name__` is `"__main__"` in the script you ran, and the module name in anything you imported.
- A relative import (`from .x import y`) works only inside a package. Run that file directly and you get "attempted relative import with no known parent package".
- A folder becomes a package when it contains `__init__.py`, and that file runs when anything in the package is imported.
- `from x import *` is discouraged. `from x import a, b` is fine, whatever the slide says.
- `np.percentile(x, 50)` is the median. A percentile that falls between two data points is interpolated by default.
- `print(SO.__doc__)` shows the surrounding blank lines of a triple-quoted docstring.
