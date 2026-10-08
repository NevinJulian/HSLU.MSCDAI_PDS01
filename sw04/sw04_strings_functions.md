# SW04 · String Formatting and Functions I

**Date:** 2026-10-08
**Slides:** `sw04_fstr_fnc.pdf` · **Exercises:** [SW04 exercise sheet](sw04_exercises.md)

Topics: strings as a list of characters, variables in strings (f-strings and `.format()`), format modifiers, Python functions (motivation, syntax, arguments, return values).

## Contents

1. [Strings as a list of characters](#1-strings-as-a-list-of-characters)
2. [Variables in strings](#2-variables-in-strings)
3. [Format modifiers](#3-format-modifiers)
4. [Functions: why](#4-functions-why)
5. [Structure](#5-structure)
6. [Arguments](#6-arguments)
7. [Return values](#7-return-values)
8. [Default values](#8-default-values)
9. [Summary and conventions](#9-summary-and-conventions)

---

## 1. Strings as a list of characters

Python treats a string as a sequence of characters, including single letters, symbols and escape characters. Everything from the slicing part of [SW02](../sw02/sw02_control_structures.md#10-sequence-slicing) applies.

```
li : 'H' 'e' 'l' 'l' 'o' ' ' 'w' 'o' 'r' 'l' 'd' '\n'
idx:  0   1   2   3   4   5   6   7   8   9   10   11
```

Strings:

- can be sliced: `li[:10:2]` gives `'Hlowr'`
- can be concatenated: `li[0:5] + li[6:11]` gives `'Helloworld'`
- allow index based access: `li[5]` gives `' '`
- allow formatting based on character positions: `'   lo'` is right aligned in 5 characters

`'\n'` is one character, not two, so this string has `len()` 12.

Strings are immutable. `li[0] = 'J'` raises a `TypeError`, a changed string is always a new one.

## 2. Variables in strings

Two main options for putting variables into strings.

### Option 1: leading f

| Type | Code | Output |
|---|---|---|
| named insertion | `f"hello {var1} {var2}"` | `hello 7 world` |
| self contained | `f"hello {var1=} {var2}"` | `hello var1=7 world` |

The `=` form prints the variable name together with its value, which is useful for debugging.

### Option 2: trailing .format()

| Type | Code | Output |
|---|---|---|
| order based | `"hello {} {}.".format(var1, var2)` | `hello 7 world.` |
| numbering | `"hello {1} {0}.".format(var1, var2)` | `hello world 7.` |
| keywords | `"hello {a} {b}.".format(b=var1, a=var2)` | `hello world 7.` |
| dictionary | `"hello {0[num]} {0[txt]}.".format(d)` | `hello 7 world.` |

with `var1 = 7`, `var2 = "world"` and `d = {'num': 7, 'txt': 'world'}`.

Numbering and keywords decouple the order in the string from the order of the arguments, which matters when the same value appears twice or when a translation reorders a sentence.

A dictionary can also be unpacked into keyword arguments:

```python
"hello {num} {txt}.".format(**d)
```

Two details on the slide: the outputs drop the trailing period that is part of every template, and the dictionary is named `dict`, which shadows the builtin type. Name it `d` or `insert_dict`.

f-strings are the default choice in new code. `.format()` still has its place when the template is stored somewhere else, for example in a config file or a translation table, because an f-string is evaluated where it is written.

## 3. Format modifiers

Inserted variables can be formatted in place with `{value:modifier}`.

| Modifier | Meaning | Example | Result |
|---|---|---|---|
| `>x` | right align in x characters | `f"{'lo':>5}"` | `'   lo'` |
| `<x` | left align in x characters | `f"{'lo':<5}"` | `'lo   '` |
| `.2` | precision: 2 significant digits for numbers, max length for strings | `f"{2.7182818:.2}"` | `'2.7'` |
| `.2f` | 2 decimals after the point, rounded | `f"{3.14159:.2f}"` | `'3.14'` |

**Slide error (page 6).** The line `">x" "<x" -> left align and right align with x spaces` has the two the wrong way round. `>` aligns right and `<` aligns left, which is also what the example on page 4 shows. A way to remember it: the arrow points at the side the text is pushed to.

**On `.2`:** for a string it is the maximum length (`f"{'abcdef':.2}"` gives `'ab'`), for a float it is the number of significant digits, not decimals. `f"{2.7182818:.3}"` gives `'2.72'`, while `f"{2.7182818:.3f}"` gives `'2.718'`.

Example from the slides:

```python
numbers = {"Euler": 2.7182818, "Pi": 3.1415926}

print("Irrational numbers I know:")
for label in numbers.keys():
    number = numbers[label]
    print(f"{label}: {number}")

print("Irrational numbers I know:")
for label in numbers.keys():
    number = numbers[label]
    print(f"{label:<6}: {number:.3}")
```

```
Irrational numbers I know:          Irrational numbers I know:
Euler: 2.7182818                    Euler : 2.72
Pi: 3.1415926                       Pi    : 3.14
```

The second loop pads every label to 6 characters, so the colons line up in a column. Other modifiers worth knowing: `,` as a thousands separator (`f"{1234567:,}"` gives `'1,234,567'`) and `^` for centring.

## 4. Functions: why

The starting point on the slides, three times the same three lines:

```python
base_price = 3500
modification = 1.5
selling_price = modification*base_price
print(f"Calculated price: {selling_price} CHF")

base_price = 90
modification = 1.5
selling_price = modification*base_price
print(f"Calculated price: {selling_price} CHF")

base_price = 210
modification = 1.5
selling_price = modification*base_price
print(f"Calculated price: {selling_price} CHF")
```

The block is duplicated, only `base_price` changes. Give the block a name and the varying value as a parameter:

```python
def calculate_selling_price(base_price):
    modification = 1.5
    selling_price = modification*base_price
    print(f"Calculated price: {selling_price} CHF")

calculate_selling_price(3500)
calculate_selling_price(90)
calculate_selling_price(210)
```

To use a result outside the block, return it:

```python
def calculate_selling_price(base_price):
    modification = 1.5
    selling_price = modification*base_price
    print(f"Calculated price: {selling_price} CHF")
    return selling_price

calculated_price = calculate_selling_price(5000)
print(calculated_price)
```

**Extensibility.** When the modification suddenly depends on the base price, one place changes and every call follows:

```python
def calculate_selling_price(base_price):
    if base_price > 1000:
        modification = 1.2
    else:
        modification = 1.5
    selling_price = modification*base_price
    print(f"Calculated price: {selling_price} CHF")
    return selling_price
```

In the copy-paste version this would be three edits, and in a real script thirty.

## 5. Structure

A function has a header and a body.

```python
def function_name(parameter, list):
    block instruction
    block instruction
    return value
```

**Header**

- starts with the keyword `def`
- the parameters are the input list, which can have any length or be empty

**Body**

- any number of instructions
- can call other functions and build nested structures
- ends with a return value, explicit or not

## 6. Arguments

```python
def const_slice(input_list, step):
    s = step + 3
    l = input_list[::s]
    return l

li = [1, 2, 3, 4, 5, 6, 7]
li_s = const_slice(li, 2)
```

Properties of the argument list:

- arbitrary length, or empty
- fixed order by default, so `const_slice(li, 2)` fills `input_list` and `step` in that order
- can contain optional arguments with default values: `def const_slice(input_list, step=3)`
- keywords allow a changed order: `const_slice(step=2, input_list=li)`
- the data type is not checked
- arguments are passed as references to a storage location

The last point has a consequence the slide does not spell out. A mutable argument such as a list can be changed inside the function, and the caller sees that change:

```python
def append_one(values):
    values.append(1)

my_list = []
append_one(my_list)
print(my_list)        # [1]
```

Related trap, and the reason the slides use `None` as a default on page 19: a default value is evaluated once at definition time, so a mutable default is shared between all calls.

```python
def broken(values=[]):     # never do this
    values.append(1)
    return values

broken()    # [1]
broken()    # [1, 1]
```

The fix is `def fixed(values=None):` and `if values is None: values = []` inside the body.

## 7. Return values

- a return value is a reference to a storage location, or `None`, so every function has a return value
- functions can return references to any data type, including other functions
- multiple values go back in one list or tuple: `return ['hello', 7, 'computer']`

A function without a `return` statement returns `None`. This is the usual bug behind `TypeError: 'NoneType' object is not subscriptable`, where a `print()` at the end of the function was meant to be a `return`.

Return values can be assigned, passed on, or chained:

```python
var1 = my_function(my_list)
my_wrapper(my_function(88))
my_function(88).my_wrapper()
```

Unpacking a returned tuple is the common way to get several results out:

```python
def min_max(values):
    return min(values), max(values)

low, high = min_max([3, 8, 1])
```

## 8. Default values

With a default value the caller decides whether to pass the argument at all. `None` as a default means "not given", which lets the function compute the value itself:

```python
def calculate_selling_price(base_price, modification=None):
    if modification is None:
        if base_price > 1000:
            modification = 1.2
        else:
            modification = 1.5
    selling_price = modification*base_price
    print(f"Calculated price: {selling_price} CHF")
    return selling_price

calculate_selling_price(3500)
calculate_selling_price(3500, 1.6)
calculate_selling_price(3500, modification=1.6)
```

The rule on the slide, that keyword arguments are passed after positional ones, holds for the call. The same holds for the definition: a parameter with a default cannot be followed by one without, otherwise Python raises `SyntaxError: non-default argument follows default argument`.

This is Exercises 7 and 8 of this week.

## 9. Summary and conventions

Functions combine instructions into a block that can be executed many times. The advantages:

- modularity, which removes duplication and makes code extensible
- readability
- easier debugging and testing

Hints from the slides:

- a function should tackle one particular issue
- names use snake case: `my_function()`, `value_converter()`
- functions must be defined before they are used

The last point is about execution order, not file order. The `def` has to have run before the call runs, so a function may well be called from code written above it, as long as that code executes later. The calculator in Exercise 6 is exactly this case: `main()` uses `add()` and runs at the bottom of the file.
