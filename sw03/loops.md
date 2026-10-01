# SW03 · Control Structures II

**Date:** 2026-10-01, online
**Slides:** `sw03_for_while.pdf` · **Exercises:** [SW03 exercise sheet](sw03_exercises.md)

Topics: for loop, while loop, the loop `else` condition, `break` / `continue` / `pass`, `enumerate()`, AI support for coding.

## Contents

1. [for loop](#1-for-loop)
2. [while loop](#2-while-loop)
3. [break, continue, pass](#3-break-continue-pass)
4. [enumerate()](#4-enumerate)
5. [AI and Python](#5-ai-and-python)

---

## 1. for loop

Loops iterate over sequence objects and hand each element to the loop variable one after another. The for loop:

- assigns each element of the sequence to the loop variable
- executes the body (the indented block after the colon)
- ends when the sequence has no next element

```python
x = [3, 11, -32, 18, -5]
for e in x:
    e = e + 10
    print(e)          # 13, 21, -22, 28, 5

print(x)              # [3, 11, -32, 18, -5]
```

The last line is the point of the example: `e` is a new name bound to the current element, so assigning to it does not touch the list. To change the list, write back by index, for example with [enumerate](#4-enumerate) or `x[i] = x[i] + 10`.

**Slide typo (pages 4 and 5):** the comment says the list prints as `[3,11,-32,18,5]`. The last element stays `-5`.

### else condition

A for loop can carry an `else` block. It runs when the sequence is exhausted, and it is skipped when the loop ends early:

- cause I: a `break`
- cause II: an error was raised

```python
x = [3, 11, -32, 18, -5]
for e in x:
    e = e + 10
    print(e)
else:
    print('end')      # runs after the last element
```

The block is optional. Its real use case is the search pattern: `break` when something is found, and the `else` runs only when nothing was found.

**Slide errors (page 5):** the example assigns the list to upper-case `X` but iterates over lower-case `x`, which raises a `NameError` on its own. Inside the body it says `print` without brackets, which only references the function and prints nothing. Also, an exhausted iterator raises `StopIteration` rather than having `next()` return `False`.

### Nested loops

```python
x = [3, 11, -32, 18, -5]    # 5 elements
y = [1, 2, 3, 4, 5, 6, 7]   # 7 elements
for i in x:
    for j in y:
        e = i * j
        print(e)
    print('next')           # after each full inner loop
else:
    print('end')            # after the outer loop finished
```

The inner loop runs completely for every element of the outer loop, so this body executes 5 × 7 = 35 times. Nested loops are what Exercises 1, 3 and 6 of this week are about.

### Header shortcut: unpacking

Nested sequences with a constant structure can be unpacked straight into separate loop variables. The number of variables must match the number of elements per item:

| Variables | Sequence |
|---|---|
| 2 (`x, y`) | `(['hello', 1], [66, 99], [2, 'world'])` |
| 3 (`x, y, z`) | `[[1,2,3], [4,5,6], [7,8,9], [10,11,12]]` |
| 5 (`v, w, x, y, z`) | `['hello', 'funny', 'world']` |

The third one works because a string is a sequence of characters and each of these words has exactly five of them.

```python
for a, b in (['hello', 1], [66, 99], [2, 'world']):
    print(a, b)       # hello 1 / 66 99 / 2 world
```

A mismatch raises `ValueError: not enough values to unpack`.

## 2. while loop

The while loop runs its body as long as the condition is true. It checks the condition before every pass and stops as soon as it is false.

```python
x = 1
while x < 10:
    print(x)          # 1, 2, 4, 8
    x = x * 2
print(x)              # 16, the value that broke the condition
```

The variable in the condition has to change inside the body, otherwise the loop never ends. Use a for loop when the number of passes is known in advance, and a while loop when it depends on something that happens during the loop, such as user input (Exercise 5).

### else condition

```python
x = 1
while x < 10:
    print(x)
    x = x * 2
else:
    print('end')      # condition became False
print(x)
```

As with the for loop, the `else` is skipped after a `break` or an error.

## 3. break, continue, pass

| Keyword | Effect |
|---|---|
| `break` | leaves the current loop immediately, the `else` block is skipped |
| `continue` | skips the rest of the body and jumps back to the loop header |
| `pass` | does nothing, a placeholder where a statement is syntactically required |

`break` and `continue` only affect the innermost loop. In a while loop, a `continue` that jumps over the line which changes the condition variable produces an endless loop:

```python
i = 0
while i < 5:
    if i == 2:
        continue      # i never changes again -> endless loop
    print(i)
    i = i + 1
```

`pass` is for empty blocks that are planned but not written yet. Python has no empty block, so `pass` keeps the file running.

## 4. enumerate()

`enumerate(iterable, start=0)` returns an iterator that yields a tuple of a counter and the element.

```python
li = [2, -5, 7, 23, 44]
list(enumerate(li))             # [(0, 2), (1, -5), (2, 7), (3, 23), (4, 44)]
list(enumerate(li, start=1))    # [(1, 2), (2, -5), (3, 7), (4, 23), (5, 44)]

for idx, value in enumerate(li):
    print(idx, value)
```

Advantages: the index of each element is known without a separate counter variable, and the counter can start at an offset. This is the clean way to write back into a list while looping over it:

```python
for i, value in enumerate(li):
    li[i] = value + 10
```

Docs: [enumerate](https://docs.python.org/3/library/functions.html#enumerate)

## 5. AI and Python

Modern IDEs support coding with AI in two ways:

1. **IntelliSense:** code completion, parameter info, quick info and member lists, so suggestions while typing.
2. **Integrated chatbots (GenAI):** generate content such as code from a prompt and can take project details into account (variables, structures, objectives).

Typical uses: generating code snippets, debugging and error fixing, code optimisation, learning and explanation, documentation and comments, testing and quality assurance, version control and collaboration, framework-specific help.

Quality depends on the prompt, and the programmer stays responsible for the final implementation. Possible mistakes in generated code named on the slides: logical errors, wrong assumptions about the input data format, overlooked edge cases (empty input, extreme values, invalid data), inefficient code, security holes, missing error handling, outdated libraries, ignored best practices, overcomplicated solutions, untested code.

Recommendation of the lecturers for this module, where the goal is learning Python:

- fix errors with AI only after inspecting the code yourself
- ask for an explanation of how Python interprets something
- ask for alternative solutions
- let it generate additional exercises, e.g. "Provide some simple exercises for list slicing in Python."

Disabling or restricting the AI assistant in PyCharm: [JetBrains documentation](https://www.jetbrains.com/help/ai-assistant/disable-ai-assistant.html#completely-disable-ai-assistant)
