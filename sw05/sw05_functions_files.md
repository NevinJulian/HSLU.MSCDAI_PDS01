# SW05 · Functions II, Scope, Recursion and Files

**Date:** 2026-10-15
**Slides:** `sw05_fnc_ii.pdf` (dated 14 Oct 2026) · **Exercises:** [SW05 exercise sheet](sw05_exercises.md)

Topics: packing and unpacking operators, `*args` and `**kwargs`, mutable arguments, global and local variables, `global` and `nonlocal`, recursion, file handling.

## Contents

1. [Packing and unpacking: * and **](#1-packing-and-unpacking--and-)
2. [Flexible arguments: *args and **kwargs](#2-flexible-arguments-args-and-kwargs)
3. [Mutable data types in functions](#3-mutable-data-types-in-functions)
4. [Local and global variables](#4-local-and-global-variables)
5. [Keyword: global](#5-keyword-global)
6. [Keyword: nonlocal](#6-keyword-nonlocal)
7. [Recursion](#7-recursion)
8. [File handling](#8-file-handling)

---

## 1. Packing and unpacking: * and **

`*` and `**` either pack or unpack a data collection, depending on where they are used.

### Assignments (packing)

```python
a, b, c, d = 1, 2, 3, 4
a, b, c, d = (1, 2, 3, 4)

a, *b = 1, 2, 3, 4
# -> a = 1, b = [2, 3, 4]

a, *b, c = 1, 2, 3, 4
# -> a = 1, b = [2, 3], c = 4
```

A starred name collects everything the other names do not take. Only one star is allowed per assignment, otherwise the split is ambiguous.

**Slide error (page 4).** The comments say `b = (2, 3, 4)` and `b = (2, 3)`, written as tuples. A starred assignment target always produces a **list**, never a tuple, even when the right side is a tuple. Verified on Python 3.13:

```python
>>> a, *b = 1, 2, 3, 4
>>> b, type(b)
([2, 3, 4], <class 'list'>)
```

### Calls (unpacking)

```python
a = [1, 2]
b = [3, 4]

c = [a, b]
# -> c = [[1, 2], [3, 4]]     nested
c = [*a, *b]
# -> c = [1, 2, 3, 4]         flattened

d1 = {"a": 1}
d2 = {"b": 2}
d12 = {**d1, **d2}
# -> d12 = {"a": 1, "b": 2}
```

`*` spreads a sequence into the surrounding collection, `**` spreads a dictionary. Merging dictionaries this way, the **later** key wins if both have it.

## 2. Flexible arguments: *args and **kwargs

The same concept applies to function arguments, so a function can take an undefined number of elements. Where there is no reason to pick other names, the convention is `*args` for positional and `**kwargs` for keyword arguments. The stars do the work, the names are free.

```python
def adder(*numbers):
    result = 0
    for elem in numbers:
        result += elem
    return result

print(adder(1, 2))        # -> 3
print(adder(1, 2, 2.6))   # -> 5.6
```

`**` packs keywords into a dictionary. Inside the function `args` is an ordinary tuple and `kwargs` an ordinary dictionary:

```python
def flexible_fun(*args, **kwargs):
    print(args)
    print(kwargs)

flexible_fun("Hello", "World", one=1, two=2)
# -> ('Hello', 'World')
# -> {'one': 1, 'two': 2}
```

Hints from the slides:

- Mixing positional arguments, `*args`, arguments with default values and `**kwargs` is possible.
- `**dict` can also be used in the **call** of a function. The labels then have to match the argument names.

The order in the definition is fixed: positional, then `*args`, then keyword-only arguments with defaults, then `**kwargs`.

```python
def f(a, *args, mode="fast", **kwargs):
    ...
```

**You have been using this all along.** `print` is defined as

```python
print(*objects, sep=' ', end='\n', file=None, flush=False)
```

`*objects` packs however many elements you pass into a tuple, which is why `print("a", "b", "c")` works without `print` knowing in advance how many arguments arrive. See the [docs](https://docs.python.org/3/library/functions.html#print).

## 3. Mutable data types in functions

Variables defined inside a function normally do not affect anything outside it. Mutable data types are the exception: they allow changes, and Python passes references, so a change made inside the function survives the call.

```python
def adder(p):
    p = p + 1
    return p

int_var = 3
print(adder(int_var))   # -> 4
print(int_var)          # -> 3
```

```python
def list_manipulator(c_list):
    c = c_list
    c[-1] = 99
    return c

list_var = [1, 2, 3]
print(list_manipulator(list_var))   # -> [1, 2, 99]
print(list_var)                     # -> [1, 2, 99]
```

`p` refers to an **immutable** type. `p = p + 1` builds a fresh integer and rebinds the local name, leaving `int_var` alone. `c_list` refers to a **mutable** type. `c = c_list` does not copy anything, it is a second name for the same list, so `c[-1] = 99` changes the caller's list.

The rule to carry: **rebinding a name is local, mutating an object is not.** `p = p + 1` rebinds. `c[-1] = 99` mutates. Mutable types are `list`, `dict`, `set` and most custom objects. Immutable are `int`, `float`, `str`, `tuple`, `bool`, `frozenset`.

To work on a copy instead:

```python
c = c_list[:]          # or list(c_list), or c_list.copy()
```

That is a shallow copy. Nested lists inside it are still shared, `copy.deepcopy()` handles those. Shallow versus deep copy comes up again in SW10.

## 4. Local and global variables

| | Where defined | Visible |
|---|---|---|
| **global** (free) variable | Main level, or in any control statement including iterator variables of `if-else`, `match-case`, `for` and `while` | Everywhere in the script |
| **local** variable | Inside a particular function block, including its parameters | Only within that function block |

```python
welcome = 'hello world'     # global
numbers = [1, 2, 3, 4, 5]   # global
list_sum = 0                # global
for i in numbers:           # global
    list_sum += i
    last_element = i        # global
print(welcome)
print('sum: ', list_sum)
print(f'{last_element=}')
print(f'last iterator:{i}')
```

```python
welcome = 'hello world'     # global
numbers = [1, 2, 3, 4, 5]   # global

def sum_list(list_ref):     # local
    list_sum = 0            # local
    for i in list_ref:      # local
        list_sum += i
    return list_sum

print(welcome)
print('sum: ', sum_list(numbers))
```

The point of the left example: a `for` loop is **not** a scope in Python. Both `last_element` and the loop variable `i` still exist after the loop ends and are perfectly usable. Only a function body creates a new scope. That differs from most C-style languages, where the loop variable dies with the loop.

In the right example `list_sum` and `i` vanish when `sum_list` returns, and the result travels out through `return`. That is the form to prefer.

## 5. Keyword: global

Sometimes it is useful to break the rules of functional style and update a global variable from inside a function. That is a **side effect**.

Typical applications named on the slides: a global access counter or sum, a global buffer index, a global file name variable.

```python
access_cnt = 0
buffer_name = 'b_name'

def read_buffer():
    global access_cnt
    access_cnt += 1
    with open(buffer_name) as f:
        new_content = f.readlines()
    return new_content
```

The global variable is accessed by a local re-declaration with `global`. For functional style, avoid it wherever possible.

**Slide error (page 11).** The slide writes `with open('b_name') as f:`, with the file name in quotes. That opens a file literally called `b_name` and never touches `buffer_name`, which defeats the "global file name variable" the example is meant to demonstrate. It has to be `open(buffer_name)`, as corrected above.

Why `global` is needed at all: **reading** a global works without any declaration. Only **assigning** to a name inside a function makes it local for the whole function body, which is what breaks `access_cnt += 1` with an `UnboundLocalError`. The `global` statement switches that off.

Note that mutating a global list or dictionary needs no `global`, because `my_list.append(x)` is a mutation, not an assignment. Same rule as in [section 3](#3-mutable-data-types-in-functions).

[Docs](https://docs.python.org/3/reference/simple_stmts.html#the-global-statement)

## 6. Keyword: nonlocal

A local namespace may contain another local namespace, which is the case for a nested function. `nonlocal` reaches into the parent's namespace.

```python
x = 99                       # global
def bar():
    x = 1                    # local
    print(x)
    def foo():
        nonlocal x           # local
        x = 55               # local
        y = 77               # nested local
        print(x)
        print(y)
    foo()
    print(x)
print(x)
bar()
print(x)
```

Output:

```
99
1
55
77
55
99
```

- Accessing an object of the parent namespace requires a re-declaration: `nonlocal parent_variable`
- A nonlocal declaration **cannot** carry a value assignment: `nonlocal x = 55` is a `SyntaxError`

The last two lines are the point of the example. `foo` changes `bar`'s `x` to 55, so `bar` prints 55 after the call, but the module-level `x` is untouched and still prints 99. `nonlocal` climbs exactly one level of enclosing **function**, it never reaches the global scope. For that there is `global`.

## 7. Recursion

From Late Latin *recursiō*, a running back, 1925–30. In programming it means a function that calls itself.

**Advantage.** For data scientists it is useful to loop through a data set with undefined dimension and undefined iteration count:

- simple iteration through tree-like structures
- concise implementation

**Disadvantage:**

- hard to implement and debug
- resource intensive
- risk of memory overflow

### Factorial

```python
def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n-1)
```

`factorial(5)` gives 120. Every recursion needs two parts: a **base case** that returns without recursing, and a **recursive case** that moves towards it. Here the base case is `n == 1` and each call shrinks `n` by one.

**Slide issue.** The base case `n == 1` does not catch `n = 0`. `factorial(0)` counts down through 0, -1, -2 and never reaches 1, ending in a `RecursionError`. Mathematically 0! = 1, so the base case should be:

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
```

### Recursive bubble sort

```python
def my_sort(li):
    for i in range(len(li)-1):
        if li[i] > li[i+1]:
            # -> if true, swap positions
            # -> and recall on updated list
            li[i], li[i+1] = li[i+1], li[i]
            li = my_sort(li)
    return li
```

Bubble sort normally needs a nested for-loop and careful indexing. Here one pass swaps a neighbouring pair and then hands the updated list to a fresh call, so the recursion replaces the outer loop.

Two things the slide does not say:

- **It sorts in place.** `li[i], li[i+1] = ...` mutates the caller's list, exactly as in [section 3](#3-mutable-data-types-in-functions). The returned list is the same object that went in, so the original is sorted too.
- **It runs out of stack quickly.** The recursion depth grows roughly with the square of the list length. Measured against Python's default limit of 1000: a reversed list of 45 elements still works, 46 raises a `RecursionError`. Fine as a teaching example, unusable on real data. `sorted()` is the answer in practice.

Python has no tail call optimisation, so every recursive call keeps a frame on the stack. `sys.setrecursionlimit()` raises the limit but not the actual stack, so pushing it far enough crashes the interpreter. When a recursion is really just a loop, write the loop.

## 8. File handling

Files store data outside the application, which lets you keep information for the next execution and share data between applications.

Python accesses a file through a **file object**:

```python
file_object = open(file_name, mode)
```

The programmer who opens a file is also responsible for closing it:

```python
file_object.close()
```

Python takes over that responsibility if the access is handled with `with`:

```python
with open(file_name, mode) as file_object:
    ...
```

Use `with` always. It closes the file even when an exception is raised in the middle of the block.

### Modes

| mode | Meaning |
|---|---|
| `'r'` | open for reading (default) |
| `'w'` | open for writing, truncating the file first |
| `'x'` | open for exclusive creation, failing if the file already exists |
| `'a'` | open for writing, appending to the end of file if it exists |
| `'b'` | binary mode |
| `'t'` | text mode (default) |
| `'+'` | open for updating (reading and writing) |

The first group is combined with the second, so `'rb'` reads binary and `'w+'` opens for reading and writing with truncation. **`'w'` deletes the content of an existing file the moment it opens**, before anything is written. `'x'` is the safe variant when the file must not already exist.

### Reading

Three objectives, with the matching call:

```python
content = file_object.read(size)      # 1. a certain quantity of data

while content not condition:          # 2. line by line
    content = file_object.readline()

for line in file:
    ... line

content = file_object.read()          # 3. the whole file at once
```

`file_object.readlines()` or `list(file_object)` return all lines in a list.

- `read(size)` returns the entire content when `size` is empty or negative
- if `read` returns the entire content, **Python does not care about the memory size**
- when `read` has reached the end of file it returns an empty string `''`

That empty string is how the loop in form 2 terminates, since `''` is falsy. Note that a line containing only a newline is `'\n'`, which is **not** empty and not the end of the file.

Looping directly over the file object, form 2 on the right, is the idiomatic version. It reads one line at a time, so memory use stays flat whatever the file size, which is exactly the warning in the third bullet. Every line keeps its trailing `\n`, so `.strip()` is almost always needed.

### Writing

Writing is more critical than reading. Data written to a file goes through a **buffer** that writes packages to the file:

```
"hello world"  ->  'h' 'e' 'l' 'l' 'o' ' ' 'w' 'o' 'r' 'l' 'd'
```

The buffer means the write is unfinished as long as the stream is not flushed, by either:

1. `file_object.flush()`
2. `file_object.close()`

`with open(file_name) as f:` closes the file object and flushes the stream when the block finishes.

```python
with open(file_name, 'w') as file:
    file.write('hello world')
```

The practical consequence: a program that writes a file and then crashes, or that is killed before closing, can leave an empty or truncated file even though `write()` returned without error. `write()` does not append a newline, unlike `print()`, so line breaks have to be written explicitly. `writelines(list)` writes a list of strings and adds no newlines either.

[Docs: reading and writing files](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)
