# SW02 · Exercise sheet: Conditionals

**Sheet:** `exercises.pdf` · **Theory:** [SW02 notes](sw02_control_structures.md)

All solutions below were run on Python 3.12. Solutions are collapsed, try the task first.

---

## Exercise 1: Day of the week

Ask for a number between 1 and 7 (1 = Monday, …, 7 = Sunday) and print:

- `You have to work ...!` for Monday to Friday
- `Enjoy your weekend...!` for Saturday and Sunday
- `Wrong input...!` for any other number

<details>
<summary>Solution</summary>

```python
day = int(input("Number of the day (1-7): "))

if 1 <= day <= 5:
    print("You have to work ...!")
elif day in (6, 7):
    print("Enjoy your weekend...!")
else:
    print("Wrong input...!")
```

The chained comparison `1 <= day <= 5` is the readable form of `day >= 1 and day <= 5`.

Same thing with match-case:

```python
match day:
    case 1 | 2 | 3 | 4 | 5:
        print("You have to work ...!")
    case 6 | 7:
        print("Enjoy your weekend...!")
    case _:
        print("Wrong input...!")
```

Note that `int(input(...))` raises a `ValueError` if the user types text instead of a number. Catching that needs `try/except`, which comes in SW12.

</details>

## Exercise 2: Customer categories

Divide adult customers into four categories by age:

| Age | Category |
|---|---|
| 18 ≤ age < 25 | Youth |
| 25 ≤ age < 35 | YoungAdult |
| 35 ≤ age < 60 | MiddleAged |
| 60 ≤ age | Senior |

Output for a 22 year old customer: `The customer belongs to the 'Youth' category!`

<details>
<summary>Solution</summary>

```python
age = int(input("Age of the customer: "))

if age < 18:
    category = None
elif age < 25:
    category = "Youth"
elif age < 35:
    category = "YoungAdult"
elif age < 60:
    category = "MiddleAged"
else:
    category = "Senior"

if category is None:
    print("The customer is not an adult, no category defined!")
else:
    print(f"The customer belongs to the '{category}' category!")
```

The elif chain only needs the upper bound of each category, because a branch is only reached when all previous ones were false. Writing `elif 25 <= age < 35:` is correct too, just redundant.

The task says adult customers, but the rules say nothing about an age below 18, so the program handles that case separately instead of silently calling a 12 year old a `Youth`.

</details>

## Exercise 3: Temperature conversion

Convert between Celsius and Fahrenheit, with

$$T_C = \frac{5}{9} \cdot (T_F - 32)$$

Write both directions and combine them into one program with an additional input for the direction, e.g. `F` and `45` for Fahrenheit to Celsius.

<details>
<summary>Solution</summary>

Solving the given equation for the other direction gives $T_F = \frac{9}{5} \cdot T_C + 32$.

```python
direction = input("Direction (C = Celsius to Fahrenheit, F = Fahrenheit to Celsius): ").strip().upper()
value = float(input("Temperature: "))

match direction:
    case "C":
        print(f"{value} C = {value * 9/5 + 32:.2f} F")
    case "F":
        print(f"{value} F = {5/9 * (value - 32):.2f} C")
    case _:
        print("Wrong direction...!")
```

`.strip().upper()` makes the input tolerant to a space or a lower case letter. Check points: 0 C = 32 F, 100 C = 212 F, 45 F = 7.22 C, and -40 is the same in both scales.

Use `float()` and not `int()` here, temperatures are rarely whole numbers. Write `value * 9/5` and not `value * (9//5)`, integer division would give 1.

</details>

## Exercise 4: Three numbers in ascending order

Ask for three whole numbers (also negative) and print them in ascending order. Use nested if-statements, no built-in `sort`.

<details>
<summary>Solution</summary>

```python
a = int(input("First number: "))
b = int(input("Second number: "))
c = int(input("Third number: "))

if a <= b:
    if b <= c:
        print(a, b, c)
    elif a <= c:
        print(a, c, b)
    else:
        print(c, a, b)
else:
    if a <= c:
        print(b, a, c)
    elif b <= c:
        print(b, c, a)
    else:
        print(c, b, a)
```

Three numbers have six possible orders, and the structure above reaches each of them with at most two comparisons. Using `<=` instead of `<` keeps equal values working.

Checked against `sorted()` for every combination of three values from -3 to 3, including duplicates, with no mismatch.

</details>

## Exercise 5: Conditional expression I

`a`, `b` and `c` are initialised ints. Find `EXPR` so that the block runs when:

> a is greater than b | a is less than half of b | the sum of a and c is greater than b

Check: `a=1, b=2, c=2` → True, and `a=1, b=2, c=1` → False.

<details>
<summary>Solution</summary>

```python
if a > b or a < b / 2 or a + c > b:
    print("Condition fulfilled.")
```

| a | b | c | a > b | a < b/2 | a + c > b | Result |
|---|---|---|---|---|---|---|
| 1 | 2 | 2 | False | False | True (3 > 2) | **True** |
| 1 | 2 | 1 | False | False | False (2 > 2) | **False** |

"Half of b" is `b / 2`. With `b // 2` both test cases also pass, but the two differ for odd values of b: with `b = 5`, `a = 2` is less than 2.5 but not less than 2.

</details>

## Exercise 6: Conditional expression II

`a`, `b` and `c` are initialised ints. Find `EXPR` so that the block runs when:

> a/2 is an odd number | b − c is an even number | both a and b and also b and c have different values

Check: `(6,2,0)` → True, `(5,2,1)` → True, `(5,5,2)` → False, `(4,4,1)` → False.

<details>
<summary>Solution</summary>

```python
if (a // 2) % 2 or not (b - c) % 2 or (a != b and b != c):
    print("Condition fulfilled.")
```

| a | b | c | a//2 odd | b-c even | a≠b and b≠c | Result | Expected |
|---|---|---|---|---|---|---|---|
| 6 | 2 | 0 | True (3) | True (2) | True | **True** | True |
| 5 | 2 | 1 | False (2) | False (3) | True | **True** | True |
| 5 | 5 | 2 | False (2) | False (3) | False (a = b) | **False** | False |
| 4 | 4 | 1 | False (2) | False (3) | False (a = b) | **False** | False |

Reading the first condition: the PDF renders it as `a` over `2`, which can be read as a² or as a/2. **It has to be a/2.** With a² the case `(5,5,2)` would give True (25 is odd), but the sheet expects False. So the first condition is the integer division `a // 2`, checked for oddness.

`x % 2` is `1` for odd numbers, which is truthy, so `(a // 2) % 2` already works as a condition. For even numbers, `not (b - c) % 2` is the negation of that. Writing it explicitly as `(a // 2) % 2 == 1` and `(b - c) % 2 == 0` is longer but easier to read in an exam.

Note that the third condition only excludes `a == b` and `b == c`. `a` and `c` may be equal, as in `(5,2,5)`.

</details>

---

## Notes for the exam

- `x % 2` is `0` for even numbers, so `not x % 2` is true for **even** x. The slides have this backwards in two places (see the [notes](sw02_control_structures.md#elif)).
- `|` in the exercise text means "or" in prose. In code `|` is the bitwise operator, use `or`.
- `input()` always returns a string, cast it before comparing with numbers.
- Chained comparisons (`1 <= day <= 5`) and membership tests (`day in (6, 7)`) shorten conditions a lot.
