# SW04 · Exercise sheet: Print and Format, Functions

**Sheet:** `exercises.pdf` · **Theory:** [SW04 notes](sw04_strings_functions.md) · **Notebook:** [sw04_exercises.ipynb](sw04_exercises.ipynb)

The sheet is headed "Exercise Sheet SW5", but its content is the SW04 lecture (string formatting and functions), so it lives in this folder.

All solutions below were run on Python 3.13. Solutions are collapsed, try the task first.

---

## Exercise 1: f-string

Use the `f"XXX"` syntax to produce this output:

```
Hello Andreas and Ramon!
```

based on the given variables:

```python
var1 = "and"
var2 = "Andreas"
var3 = "!"
var4 = "Dear Hello"
var5 = "Ramona"
```

<details>
<summary>Solution</summary>

Neither `var4` nor `var5` fits as it is, both need slicing:

```python
print(f"{var4[5:]} {var2} {var1} {var5[:-1]}{var3}")
```

`var4[5:]` cuts off `"Dear "` and leaves `"Hello"`, `var5[:-1]` drops the last character of `"Ramona"`. Negative indices work just as well:

```python
print(f"{var4[-5:]} {var2} {var1} {var5[0:5]}{var3}")
```

The exclamation mark is appended without a space, everything else is separated by the spaces inside the f-string.

</details>

## Exercise 2: .format()

Use the `"XXX".format()` syntax to produce this output:

```
My name is Giacomo, I am 10 years old, and I live in Padova.
```

based on the given dictionary, once per variant: order based, number based, keyword based, dictionary-key based.

```python
insert_dict = {'name':'Giacomo', 'age':'10', 'city':'Padova'}
```

<details>
<summary>Solution</summary>

```python
insert_dict = {'name': 'Giacomo', 'age': '10', 'city': 'Padova'}

# order based
print("My name is {}, I am {} years old, and I live in {}.".format(
    insert_dict['name'], insert_dict['age'], insert_dict['city']))

# number based
print("My name is {0}, I am {1} years old, and I live in {2}.".format(
    insert_dict['name'], insert_dict['age'], insert_dict['city']))

# key-word based
print("My name is {name}, I am {age} years old, and I live in {city}.".format(**insert_dict))

# dictionary-key based
print("My name is {0[name]}, I am {0[age]} years old, and I live in {0[city]}.".format(insert_dict))
```

The keyword version can also be written out in full, `.format(name=insert_dict['name'], ...)`. `**insert_dict` unpacks the dictionary into exactly those keyword arguments, which only works because the keys match the placeholder names.

In the dictionary version, `0` refers to the first argument and `[name]` indexes into it. Note that there are no quotes around the key inside the format string, `{0['name']}` raises a `KeyError`.

</details>

## Exercise 3: Pairs from a list

Given a list of n (even) numbers, print for each pair `[(first, last), (second, second last), ...]` the string `X times Y is: X*Y`.

Calculate the product in place, inside the string in the print statement.

<details>
<summary>Solution</summary>

```python
numbers = [2, 3, 5, 7, 11, 13]

for i in range(len(numbers) // 2):
    print(f"{numbers[i]} times {numbers[-1 - i]} is: {numbers[i] * numbers[-1 - i]}")
```

```
2 times 13 is: 26
3 times 11 is: 33
5 times 7 is: 35
```

The loop runs over the first half of the list, `numbers[-1 - i]` walks backwards from the end. Half the length is enough, running over the whole list would print every pair twice.

An f-string evaluates any expression inside the braces, so `{numbers[i] * numbers[-1 - i]}` is the in-place calculation the task asks for.

Walking from both ends at once also works and is easier to read:

```python
for a, b in zip(numbers, reversed(numbers)):
    print(f"{a} times {b} is: {a * b}")
```

but that prints all pairs, so it needs a stop after half the list.

</details>

## Exercise 4: Even numbers

Write a function that accepts a list of integers and returns a list with all even numbers of the input list.

<details>
<summary>Solution</summary>

```python
def even_numbers(values):
    result = []
    for value in values:
        if value % 2 == 0:
            result.append(value)
    return result

print(even_numbers([1, 2, 3, 4, 5, 6, -2, 0]))   # [2, 4, 6, -2, 0]
```

The result list is created inside the function, not as a default argument. `value % 2 == 0` is true for negative even numbers and for `0` as well.

</details>

## Exercise 5: Unique values

Write a function that accepts a list and returns the unique values of that list as a list.

Hint: `set` may be used to check the result, but not inside the function.

<details>
<summary>Solution</summary>

```python
def unique_values(values):
    result = []
    for value in values:
        if value not in result:
            result.append(value)
    return result

print(unique_values([1, 1, 2, 3, 2, 'a', 'a']))   # [1, 2, 3, 'a']
print(set([1, 1, 2]))                             # {1, 2}
```

`in` checks membership of the list built so far, so every value is appended at most once. Unlike `set`, this keeps the original order and also works for unhashable elements such as lists.

The cost is quadratic, because each `in` scans the whole result. Fine for exercise sizes, slow for a million elements.

</details>

## Exercise 6: Calculator

Create a simple calculator with functions to add, subtract, multiply and divide two numbers. Implement the missing parts so that the given `main()` runs without an error.

```python
# implement missing functions here ...

def main():
    print("Select operation.")
    print("1.Add")
    print("2.Subtract")
    print("3.Multiply")
    print("4.Divide")

    choice = input("Enter choice(1/2/3/4):")
    num1 = int(input("Enter first number: "))
    num2 = int(input("Enter second number: "))

    if choice == '1':
        print(num1, "+", num2, "=", add(num1, num2))
    elif choice == '2':
        print(num1, "-", num2, "=", subtract(num1, num2))
    elif choice == '3':
        print(num1, "*", num2, "=", multiply(num1, num2))
    elif choice == '4':
        print(num1, "/", num2, "=", divide(num1, num2))
    else:
        print("Invalid input")

main()
```

<details>
<summary>Solution</summary>

```python
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    return a / b
```

The four functions go above `main()`, the rest of the file stays as given.

Two observations:

- `main()` is called at the bottom of the file, so by then every `def` has run. The functions themselves are used inside `main()`, which is defined before them in the file and still works, because the body only executes at call time.
- `divide(1, 0)` raises a `ZeroDivisionError`. Catching that needs `try/except` from SW12, a check with `if b == 0` works today.

`choice` is compared as a string (`'1'`), because `input()` always returns a string, while `num1` and `num2` are cast with `int()`.

</details>

## Exercise 7: Keyword arguments

We want the circumference of a rectangle with width = 2. What is the problem with the call `circumference(2)`?

```python
def circumference(length = 2, width = 1):
    return 2 * (length + width)

c1 = circumference(2)    # 2 should be the width !!!
print(c1)

# or with length 5 and width 3:
c2 = circumference(......)
print(c2)

# how can the function be called alternatively, for the same result?
c3 = circumference(.......)
print(c3)
```

<details>
<summary>Solution</summary>

**The problem.** `circumference(2)` passes 2 positionally, and the first parameter is `length`. So it computes `2 * (2 + 1) = 6` with the default width of 1, instead of the wanted width of 2. The call runs without an error, which makes this kind of bug easy to miss.

**Task 1:** name the argument.

```python
c1 = circumference(width=2)      # 2 * (2 + 2) = 8
```

**Task 2:** length 5 and width 3, with two different calls.

```python
c2 = circumference(5, 3)                  # positional, 16
c3 = circumference(length=5, width=3)     # by keyword, 16
```

Further variants that give the same result:

```python
circumference(width=3, length=5)    # keywords may be reordered
circumference(5, width=3)           # positional first, then keyword
```

`circumference(width=3, 5)` does not work. A positional argument can never follow a keyword argument.

</details>

## Exercise 8: Default values

Change the two definitions so that all the calls below run without an error.

```python
# Change definitions...
def hello (name):
    print ("Hello" + name + "!")

def circumference (length, width):
    return 2 * (length + width)

# ...such that this part needs to run without errors:
hello("Peter")
hello()
c1 = circumference(5, 3)
print(c1)
c2 = circumference(5)
print(c2)
c3 = circumference()
print(c3)
```

<details>
<summary>Solution</summary>

Every parameter that may be left out needs a default value:

```python
def hello(name="World"):
    print("Hello" + name + "!")


def circumference(length=2, width=1):
    return 2 * (length + width)
```

```
HelloPeter!
HelloWorld!
16
12
6
```

`circumference(5)` fills `length` and keeps the default width, so `2 * (5 + 1) = 12`. `circumference()` uses both defaults.

The parameters of `circumference` both need a default, because `c3` passes nothing. A default on `width` alone would be enough for `c2` but not for `c3`.

The given `print("Hello" + name + "!")` has no space between the words, hence `HelloPeter!`. The task does not ask for it, but `print(f"Hello {name}!")` is the better line.

</details>

---

## Notes for the exam

- `>` aligns right, `<` aligns left. The slide has this swapped.
- `.2` is significant digits for a number and maximum length for a string, `.2f` is two decimals.
- Positional arguments first, keyword arguments after, in the call and in the definition.
- A function without `return` returns `None`.
- Never use a mutable default such as `def f(values=[])`, use `None` and create the list inside.
