# SW02 · Control Structures I

**Date:** 2026-09-24, online
**Slides:** `sw02_if_else.pdf` (dated 23 Sep 2026) · **Exercises:** [SW02 exercise sheet](sw02_exercises.md)

Topics: sequential data types (repetition), type casting, input and output, boolean operations, indentation and syntax, if-else, match-case, `range()`, `len()`, sequence slicing.

## Contents

1. [Sequential data types](#1-sequential-data-types-repetition)
2. [Type casting](#2-type-casting)
3. [Input and output](#3-input-and-output)
4. [Boolean operations](#4-boolean-operations)
5. [Indentation and syntax](#5-indentation-and-syntax)
6. [If-else statement](#6-if-else-statement)
7. [Match-case statement](#7-match-case-statement)
8. [range() object](#8-range-object)
9. [len()](#9-len)
10. [Sequence slicing](#10-sequence-slicing)

---

## 1. Sequential data types (repetition)

Sequential data types may contain mixed data types and can have multiple dimensions.

| Type | Example | Properties |
|---|---|---|
| List | `li = [1,'hello',2,[4,6,'a'],(3,9)]` | ordered, mutable |
| Tuple | `tp = (77,(55,1),9,37)` or `tp = 77,(55,1),9,37` | ordered, immutable |
| Dictionary | `di = {'a':1, 'b':2, 'c':{'aa':11, 'bb':22}}` | key-value pairs, ordered, mutable, keys must be hashable (immutable), no duplicate keys |
| Set | `se = {1,28,6,(18,88),11}` | no duplicates, unordered, unindexed, only hashable elements |

Dictionaries keep insertion order since Python 3.7. Sets have no order at all, so they cannot be indexed or sliced.

## 2. Type casting

Depending on the operation, the same data has to appear in different types. String concatenation needs a string representation of every part:

```python
"hello " + 1 + "st world"        # TypeError
"hello " + str(1) + "st world"   # works
f"hello {1}st world"             # f-string, usually the better option
```

What the conversion functions accept (checked on Python 3.12):

| Call | Result |
|---|---|
| `int('3')` | `3` |
| `int(0x13)` | `19` (`0x13` is already an int literal) |
| `int(3.141592)` | `3` (cuts off, does not round) |
| `int('3.1415')` | `ValueError` |
| `int(3+3j)` | `TypeError` |
| `int('hello')` | `ValueError` |
| `float('3.1415')` | `3.1415` |
| `float(3)` | `3.0` |
| `float(3+3j)` | `TypeError` |
| `str(0x13)` | `'19'` |
| `bool('3')`, `bool(0x13)`, `bool(-3.1415)` | `True` |
| `complex('3')` | `(3+0j)` |
| `complex('3+3j')` | `(3+3j)` |

Two traps worth remembering:

- `int('3.1415')` fails, even though `int(3.1415)` works. For a decimal string use `int(float('3.1415'))`.
- `int()` on a float truncates toward zero: `int(-3.9)` is `-3`, not `-4`. Use `round()` if you want nearest.

Everything that is not `0`, `""`, `None`, empty or `False` evaluates to `True`.

## 3. Input and output

`input(prompt)` reads from standard input:

- prints `prompt` to the terminal without a trailing newline
- returns what the user typed **as a string**, without the trailing newline
- cast the result if you need a number: `age = int(input("Age: "))`

`eval()` evaluates a Python expression given as string, e.g. `eval("3+5")` returns `8`. Useful when an expression itself is the input, but it executes arbitrary code, so never run it on input you do not control. For data such as lists or numbers, `ast.literal_eval()` is the safe variant.

`print(*objects, sep=' ', end='\n', file=None, flush=False)`:

| Parameter | Meaning |
|---|---|
| `*objects` | one or more elements to print |
| `sep` | string written between the elements |
| `end` | trailing string, newline by default |
| `file` | file object with a `write(string)` method |
| `flush` | force flushing of the stream |

```python
print("a", "b", sep="-", end="!\n")   # a-b!
```

Docs: [input](https://docs.python.org/3/library/functions.html#input), [print](https://docs.python.org/3/library/functions.html#print)

## 4. Boolean operations

A boolean expression has two states only: `True` or `False`. Python treats everything that is not empty, `0`, `False` or `None` as `True`.

| Operator | Priority | Meaning |
|---|---|---|
| `not x` | 1 | `True` if x is false, else `False` |
| `x and y` | 2 | x if x is false, else y |
| `x or y` | 3 | x if x is true, else y |

Priority 1 binds tightest, so `not a and b` means `(not a) and b`. Both `and` and `or` are **short-circuit** operators: `or` only evaluates the second argument if the first is false, `and` only if the first is true.

| `or` | True | False |
|---|---|---|
| **True** | True | True |
| **False** | True | False |

| `and` | True | False |
|---|---|---|
| **True** | True | False |
| **False** | False | False |

`and` and `or` return one of their operands, not necessarily a bool: `0 or "x"` returns `"x"`.

**Bitwise operators** work on the bits of integers and are not boolean operators:

| Operation | Result |
|---|---|
| `x \| y` | bitwise or |
| `x ^ y` | bitwise exclusive or |
| `x & y` | bitwise and |
| `x << n` | x shifted left by n bits |
| `x >> n` | x shifted right by n bits |
| `~x` | bits of x inverted |

The exercise sheet uses `|` in prose for "or". In code the two are not interchangeable: `2 or 1` returns `2`, while `2 | 1` returns `3`.

**Comparison operators:** `<`, `<=`, `>`, `>=`, `==`, `!=`, `is`, `is not`. Comparisons can be chained arbitrarily: `x < y <= z` is equivalent to `x < y and y <= z`, and `z` is not evaluated at all once `x < y` is false.

**Slide error (page 13).** The slide says that `not x == y` is different from `not (x == y)`. They are identical, because comparison binds tighter than `not`. What really differs is `x == not y`, which is a `SyntaxError` and needs brackets: `x == (not y)`.

## 5. Indentation and syntax

Code structure comes from indentation and operator priorities. Priorities can be changed by grouping with brackets:

```python
True and (False or False) and (True or False)
12 < x < 20 and not x % 2        # even number between 12 and 20
```

Blocks start with a colon and are defined by indentation. The number of spaces is arbitrary but must be constant within a block. Four spaces is the PEP 8 convention.

```
instruction                 instruction
block header:               block 1 header:
    block instruction           block 1 instruction
    block instruction           block 2 header:
instruction                         block 2 instruction
                                block 1 instruction
                            instruction
```

### The question on page 16

```python
>>> True and False or False and True or False
False
```

Why: `not` binds before `and`, `and` before `or`, so the line reads `(True and False) or (False and True) or False`. Both `and` groups contain a `False`, so everything collapses to `False`.

How to make it `True`: brackets alone cannot do it. There are 14 ways to bracket this expression and all of them evaluate to `False`, because the two `True` operands always end up in an `and` group with a `False`. An operator or an operand has to change, for example:

```python
True or False or False and True or False     # first and -> or
True and not False or False and True or False
```

## 6. If-else statement

The if-else statement executes a block when a condition is true. The `else` block is optional.

```python
x = 7
if x > 10:          # 7 > 10 is False
    print(x)        # not executed
else:
    x = x + 5       # x = 12
print(x)            # 12

if x > 10:          # 12 > 10 is True
    print(x)        # 12
else:
    x = x + 5       # not executed
print(x)            # 12
```

### elif

`elif` chains conditions on the same level instead of nesting if-statements, and can always replace an `else` that only contains another condition.

```python
x = 30
if not x % 2:       # True when x is EVEN
    x = x + 1
elif x < 10:
    x = x
else:               # x is odd and x >= 10
    x = x / 10
```

**Slide error (pages 21 and 22).** The slide comments have the parity backwards. `x % 2` is `0` for an even number, and `not 0` is `True`, so `not x % 2` is true exactly when **x is even**. With `x = 30` the first branch runs and x becomes 31, which turns an even number into an odd one. The comment "True if x not even number" and the comment "increment to even number if x == odd" on the shorthand slide both describe the opposite. For "x is odd" write `if x % 2:`.

### Shorthand (conditional expression)

When a condition only affects a single expression:

```python
x = 30
x = x + 1 if not x % 2 else x                   # 31 (increments even numbers)
x = x + 1 if not x % 2 else x if x < 10 else x / 10
print('hello world') if not x % 2 else print('end')
```

The order is `value_if_true if condition else value_if_false`. Chaining more than one `else` gets hard to read quickly, a normal if-elif-else is often the better choice.

## 7. Match-case statement

Available since Python 3.10. Instead of combining many `elif` conditions, an expression is checked against patterns.

```python
x = 2
match x:
    case 0:
        print('number is 0')
    case 1:
        print('number is 1')
    case 2:
        print('number is 2')
    case _:
        print('number unknown')
```

- `case _` is the default case
- the first matching case ends the statement, the remaining cases are not checked

### Advantage: patterns

```python
v = (5, 0)
match v:
    case (1|2|3, 0):
        print('special case')
    case (x, 0):
        print('on x-axis')
    case (0, y):
        print('on y-axis')
    case _:
        print('anything else')
```

The if-elif version of the same logic needs nested conditions and index access (`v[0]`, `v[1]`). Match-case wins on readability, maintainability and expressiveness.

### Disadvantage: conditions

Match-case matches patterns, it does not run conditional checks. Guard clauses add conditions, but that case is usually solved better with `elif`:

```python
x = 177
e = 0
match x:
    case x if 100 > x >= 10:
        e = 1
    case x if 1000 > x >= 100:
        e = 2
    case x if x >= 1000:
        e = 3
    case _:
        print('irregular number')
print(x/(10**e), "E+", e)      # 1.77 E+ 2
```

**Gotcha:** a bare name in a pattern is a capture pattern, not a comparison. `case y:` matches everything and binds the value to `y`, the same way `case _` does. To compare against a constant, use a literal (`case 2:`) or a dotted name (`case Color.RED:`).

## 8. range() object

`range(start, stop[, step])` creates a sequence object with a constant step size, used for numerical sequences such as indices or time steps.

- `start`: first value, default `0`
- `stop`: **not included**
- `step`: distance between values, default `1`
- a range only stores start, stop and step, so it needs `list()` to be displayed
- ranges support all common sequence operations except concatenation and repetition

| Expression | Result |
|---|---|
| `list(range(7))` | `[0, 1, 2, 3, 4, 5, 6]` |
| `list(range(3,11))` | `[3, 4, 5, 6, 7, 8, 9, 10]` |
| `list(range(3,-4))` | `[]` |
| `list(range(-8,3,2))` | `[-8, -6, -4, -2, 0, 2]` |
| `list(range(3,11,-2))` | `[]` |
| `list(range(3,-4,-2))` | `[3, 1, -1, -3]` |

The empty results follow one rule: with a positive step `stop` must be greater than `start`, with a negative step it must be smaller. In Python the last element is almost never included.

## 9. len()

`len()` returns the number of elements of a sequence:

- counts the first dimension only
- returns a positive integer, `0` for an empty sequence
- often used to address the last element, which has index `len(x) - 1`

```python
len([2,5,7,23,44])                            # 5
len([[2,5,7], "hello", 1, {'a':2, 'b':88}])   # 4
```

## 10. Sequence slicing

Extracting sub-sequences is one of the most frequent operations in data work, for example a moving average over a window, the daily mean temperature or the opening price of a stock series.

All examples below use:

```python
li = [2,11,16,19,48,40,30,32,9,39,40,2,14,10,18,9,10,7,43,22,19,36,35]   # len 23, indices 0..22
```

### By index

Indexing returns one single element. There is no way to pass several indices:

```python
li[[7, 11, 20]]     # TypeError
a, b, c = li[7], li[11], li[20]
```

### By slice object

`slice(start, stop, step)` describes the same set of indices as `range(start, stop, step)`. The extended indexing syntax `[start:stop:step]` creates such a slice object as well.

| Expression | Result |
|---|---|
| `li[slice(3,16,4)]` or `li[3:16:4]` | `[19, 32, 2, 9]` |
| `li[slice(21,17,-1)]` or `li[21:17:-1]` | `[36, 19, 22, 43]` |
| `li[::4]` | `[2, 48, 9, 14, 10, 19]` |

### Direction and negative indices

Indices can be positive (forward from `0`) or negative (backward from the end, where `-1` is the last element). It must hold that `start < stop` with `step > 0`, or `start > stop` with `step < 0`.

| Expression | Result |
|---|---|
| `li[3:11]` and `li[-20:-12]` | `[19, 48, 40, 30, 32, 9, 39, 40]` |
| `li[10:2:-1]` and `li[-13:-21:-1]` | `[40, 39, 9, 32, 30, 40, 48, 19]` |
| `li[17:2]`, `li[-6:2]`, `li[1:-6:-1]`, `li[-22:-7:-1]` | `[]` |

Slices cannot wrap around the ends, a wrapping slice simply returns an empty list. Wrapping has to be built with concatenation:

```python
li[-6:] + li[:2]        # [7, 43, 22, 19, 36, 35, 2, 11]
li[1::-1] + li[:-7:-1]  # [11, 2, 35, 36, 19, 22, 43, 7]
```

To include the last element, leave `stop` out (`li[-6:]`) or set it past the end (`li[-6:40]`). Out-of-range bounds are clipped in a slice, while `li[40]` raises an `IndexError`.

Slicing a list returns a new list (a shallow copy), so `li[:]` is a quick way to copy a list.
