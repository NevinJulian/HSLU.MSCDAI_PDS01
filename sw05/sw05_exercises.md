# SW05 · Exercise sheet: Files, args and kwargs

**Sheet:** `exercises.pdf` ("Exercise Sheet SW5") · **Theory:** [SW05 notes](sw05_functions_files.md) · **Notebook:** [sw05_exercises.ipynb](sw05_exercises.ipynb)

Additional material: download `musicians.txt` from ILIAS and put it next to the notebook.

All solutions below were run on Python 3.13. Solutions are collapsed, try the task first.

---

## Read and write files

### Exercise 1: Combine three lines

Write a program that combines three lines from the file `musicians.txt` into one line and writes them to standard output using `print()`. An output line should contain first name, last name and artist name or band.

The band or artist name should be printed in round brackets and in capital letters.

Example: `Marshall Bruce Mathers III (EMINEM)`

<details>
<summary>Solution</summary>

```python
with open("musicians.txt") as f:
    lines = f.readlines()

for i in range(0, len(lines), 3):
    first = lines[i].strip()
    last = lines[i + 1].strip()
    artist = lines[i + 2].strip()
    print(f"{first} {last} ({artist.upper()})")
```

The file holds one field per line, three lines per musician, so the record boundary is positional. `range(0, len(lines), 3)` with step 3 walks to the start of each record and `i + 1`, `i + 2` reach the other two fields.

`.strip()` is not optional. `readlines()` keeps the trailing `\n` on every line, so without it the output breaks across lines and the closing bracket ends up on its own.

**Streaming variant**, which never holds the whole file in memory. This is the shape the slides describe as "reading file line by line in a while loop":

```python
with open("musicians.txt") as f:
    while True:
        first = f.readline()
        if not first:
            break
        last = f.readline()
        artist = f.readline()
        print(f"{first.strip()} {last.strip()} ({artist.strip().upper()})")
```

`readline()` returns `''` at the end of the file, which is falsy, so `if not first: break` is the end-of-file test. A blank line in the middle would be `'\n'`, which is truthy, so it is not mistaken for the end.

**One caveat on the grouping.** Both versions assume the number of lines is an exact multiple of three. A stray blank line at the end of the file would shift every record after it and raise an `IndexError` in the first version. If that happens, filter the blanks out first:

```python
with open("musicians.txt") as f:
    rows = (line.strip() for line in f if line.strip())
    for first, last, artist in zip(rows, rows, rows):
        print(f"{first} {last} ({artist.upper()})")
```

Listing the same generator three times in `zip` pulls three consecutive values per round, which is the compact way to group a stream into triples.

Tested against a reconstructed `musicians.txt` in the Eminem format of the sheet, output:

```
Marshall Bruce Mathers III (EMINEM)
Stefani Joanne Angelina Germanotta (LADY GAGA)
Paul David Hewson (U2)
```

</details>

### Exercise 2: Write to a file

Change the solution of the previous exercise so that the program writes the output to a potentially newly created file `musicians2.txt`.

<details>
<summary>Solution</summary>

```python
with open("musicians.txt") as source, open("musicians2.txt", "w") as target:
    lines = source.readlines()
    for i in range(0, len(lines), 3):
        first = lines[i].strip()
        last = lines[i + 1].strip()
        artist = lines[i + 2].strip()
        target.write(f"{first} {last} ({artist.upper()})\n")
```

Three things change against exercise 1:

- Mode `"w"` on the output file. It creates the file if it does not exist, which is the "potentially newly created" part of the task, and **truncates it** if it does. Use `"x"` instead if an existing file should cause an error, `"a"` to append.
- `print(...)` becomes `target.write(...)`.
- `\n` has to be written by hand. `print` adds a line break, `write` does not, so without it the whole output ends up on one line.

A single `with` can open both files, separated by a comma. Both are closed and flushed when the block ends, which is also what makes the content actually appear on disk, see [buffering](sw05_functions_files.md#writing).

</details>

## args and kwargs

### Exercise 3: Numbered keyword arguments

Write a function that accepts an arbitrary number of keyword arguments. The function should number each keyword-value pair and print it in the format:

```
1: keyword → value
2: keyword → value
...
n: keyword → value
```

Start from this template:

```python
def print_numbered_kwargs(**kwargs):
    for ind, (key, value) in enumerate(kwargs.items()):
        pass


# print_numbered_kwargs(...)
```

a) Test what happens if you pass keyword arguments in the format `your_function(a=2, b=4)`
b) Test what happens if you pass a positional argument
c) Test what happens if you pass keyword arguments as a dictionary `{"a":2, "b": 4}`
d) Use the unpack operator `**` in the call to pass the keyword arguments formatted as a dictionary

<details>
<summary>Solution</summary>

```python
def print_numbered_kwargs(**kwargs):
    for ind, (key, value) in enumerate(kwargs.items()):
        print(f"{ind + 1}: {key} → {value}")
```

`enumerate` starts at 0, so the counter needs `ind + 1` to match the required format. The alternative is to let `enumerate` do it:

```python
for ind, (key, value) in enumerate(kwargs.items(), start=1):
    print(f"{ind}: {key} → {value}")
```

`kwargs.items()` yields `(key, value)` pairs, so `enumerate` wraps each one into `(index, (key, value))`. The brackets in `ind, (key, value)` unpack both levels in one step. Written without them you would need `ind, pair` and then `pair[0]`, `pair[1]`.

**a) Keyword arguments**

```python
print_numbered_kwargs(a=2, b=4)
```

```
1: a → 2
2: b → 4
```

Works. `**kwargs` packs the keywords into the dictionary `{'a': 2, 'b': 4}`, and since Python 3.7 that dictionary keeps the order they were passed in.

**b) A positional argument**

```python
print_numbered_kwargs(5)
```

```
TypeError: print_numbered_kwargs() takes 0 positional arguments but 1 was given
```

The function signature has only `**kwargs`, which accepts keyword arguments exclusively. It declares no positional parameters at all, hence "takes 0 positional arguments". Adding `*args` in front would let it swallow positional arguments too.

**c) A dictionary passed directly**

```python
print_numbered_kwargs({"a": 2, "b": 4})
```

```
TypeError: print_numbered_kwargs() takes 0 positional arguments but 1 was given
```

The same error as b), and that is the lesson. A dictionary handed over plainly is just one object in the first positional slot, it is not keyword arguments. The braces change nothing about how it is passed.

**d) Unpacked with ****

```python
print_numbered_kwargs(**{"a": 2, "b": 4})
```

```
1: a → 2
2: b → 4
```

Identical to a). `**` at the call site spreads the dictionary into separate keyword arguments, so the function sees `a=2, b=4` and never learns a dictionary was involved. The keys have to be valid identifiers and strings, so `**{"1a": 2}` fails.

Note the symmetry: `**` in the **definition** packs keywords into a dictionary, `**` in the **call** unpacks a dictionary into keywords. Same operator, opposite directions, as on [page 4 of the slides](sw05_functions_files.md#1-packing-and-unpacking--and-).

</details>

---

## Notes for the exam

- `*` in a definition packs, `*` in a call unpacks. Same for `**` with dictionaries.
- A starred assignment target always produces a **list**: `a, *b = 1, 2, 3` gives `b == [2, 3]`.
- A dictionary passed as `f(d)` is one positional argument. Only `f(**d)` makes it keyword arguments.
- `readlines()` keeps the `\n` on every line, so strip before formatting.
- `write()` adds no newline, `print()` does.
- Mode `"w"` truncates an existing file as soon as it is opened.
- Rebinding a name inside a function is local, mutating an object is not.
- Every recursion needs a base case that is actually reachable.
