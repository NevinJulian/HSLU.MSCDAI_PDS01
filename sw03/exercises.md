# SW03 · Exercise sheet: Loops

**Sheet:** `exercises.pdf` · **Theory:** [SW03 notes](sw03_loops.md)

All solutions below were run on Python 3.12 and produce the output asked for in the sheet. Solutions are collapsed, try the task first.

---

## Exercise 1: Star pattern

Build this pattern with nested for loops:

```
*
**
***
****
*****
****
***
**
*
```

<details>
<summary>Solution</summary>

```python
for i in range(1, 6):
    for _ in range(i):
        print("*", end="")
    print()

for i in range(4, 0, -1):
    for _ in range(i):
        print("*", end="")
    print()
```

`end=""` suppresses the newline after each star, the empty `print()` ends the line. The underscore is the usual name for a loop variable that is not used in the body.

Without the inner loop the same thing is one line shorter, but the sheet asks for nested loops:

```python
for i in range(1, 10):
    print("*" * (i if i <= 5 else 10 - i))
```

</details>

## Exercise 2: Count even and odd numbers

Count the even and odd numbers in a sequence.

```python
numbers = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
```

Expected: `Even numbers: 5`, `Odd numbers: 5`

<details>
<summary>Solution</summary>

```python
numbers = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

even = 0
odd = 0
for n in numbers:
    if n % 2:
        odd = odd + 1
    else:
        even = even + 1

print("Even numbers:", even)
print("Odd numbers:", odd)
```

`n % 2` is `1` for odd numbers, which is truthy, so no comparison is needed. This also works for negative numbers, because Python's modulo follows the sign of the divisor: `-3 % 2` is `1`.

</details>

## Exercise 3: Two-dimensional structure

Ask for `m` rows and `n` columns and build a nested list where the value in row `i` and column `j` is `i*j`.

Example with m = 3 and n = 4: `[[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 4, 6]]`

<details>
<summary>Solution</summary>

```python
m = int(input("Rows m: "))
n = int(input("Columns n: "))

matrix = []
for i in range(m):
    row = []
    for j in range(n):
        row.append(i * j)
    matrix.append(row)

print(matrix)
```

The inner list has to be created inside the outer loop. Creating it once outside and appending to it would produce one single long row.

Do not build the matrix with `[[0] * n] * m` either. That repeats a reference to the same inner list m times, so writing to one row changes all of them.

The short version with nested list comprehensions comes in SW10:

```python
matrix = [[i * j for j in range(n)] for i in range(m)]
```

</details>

## Exercise 4: Numbers with even digits only

Find all numbers between 200 and 500 (limits included) that contain even digits only.

<details>
<summary>Solution</summary>

```python
result = []
for number in range(200, 501):
    only_even = True
    for digit in str(number):
        if int(digit) % 2:
            only_even = False
            break
    if only_even:
        result.append(number)

print(result)
```

Converting the number to a string makes its digits iterable. The `break` leaves the inner loop as soon as one odd digit is found.

The same logic with the loop `else` from this week, which runs only when the inner loop was not interrupted:

```python
result = []
for number in range(200, 501):
    for digit in str(number):
        if int(digit) % 2:
            break
    else:
        result.append(number)
```

The output matches the 50 numbers printed on the sheet, from 200 to 488. 500 is inside the limits but drops out, because 5 is odd. The same holds for every number in the 300s.

</details>

## Exercise 5: Guess the number

Guess a number between 1 and 10. On a wrong guess print `to big` or `to small` and ask again, on the right guess print `Well guessed!` and end. Extension: also report the number of trials.

```python
from random import randint
random_number = randint(1, 10)
```

<details>
<summary>Solution</summary>

```python
from random import randint

random_number = randint(1, 10)

trials = 0
while True:
    guess = int(input("Your guess (1-10): "))
    trials = trials + 1
    if guess > random_number:
        print("to big")
    elif guess < random_number:
        print("to small")
    else:
        print("Well guessed!")
        print(f"Well done - you have tried it {trials} times!")
        break
```

`while True` with a `break` is the standard shape when the number of passes is unknown and the stop condition is only known inside the body.

The variant with a real condition needs a start value that cannot be the answer:

```python
guess = 0
while guess != random_number:
    guess = int(input("Your guess (1-10): "))
    trials = trials + 1
    ...
```

`randint(1, 10)` includes both limits, unlike `range(1, 10)`.

</details>

## Exercise 6: Christmas tree

Ask for the trunk-excluded height and draw the tree. The trunk is always 2 rows high, and 3 wide if the entire height is greater than 5, otherwise 1.

```
     x
    xxx
   xxxxx
  xxxxxxx
 xxxxxxxxx
xxxxxxxxxxx
    xxx
    xxx
```

<details>
<summary>Solution</summary>

```python
height = int(input("Height of the tree without trunk: "))

trunk_height = 2
trunk_width = 3 if height + trunk_height > 5 else 1
crown_width = 2 * height - 1

for i in range(height):
    stars = 2 * i + 1
    print(" " * ((crown_width - stars) // 2) + "x" * stars)

for i in range(trunk_height):
    print(" " * ((crown_width - trunk_width) // 2) + "x" * trunk_width)
```

Row `i` of the crown has `2*i + 1` characters, so the widest row is `2*height - 1`. Every row is padded with half the difference to that width, which centres it. The trunk is centred the same way.

With `height = 6` this prints exactly the tree on the sheet.

**Ambiguous rule.** "Entire height" can mean the crown plus the trunk or just the crown, and the two readings differ for heights 4 and 5:

| Height (without trunk) | Entire height = h + 2 | Trunk width, reading "h + 2" | Trunk width, reading "crown only" |
|---|---|---|---|
| 3 | 5 | 1 | 1 |
| 4 | 6 | 3 | 1 |
| 6 | 8 | 3 | 3 |

The code uses the first reading, because the input is explicitly called trunk-excluded, which implies the entire height includes the trunk. Worth asking in class.

</details>

---

## Notes for the exam

- Assigning to the loop variable does not change the sequence. Write back with an index, best via `enumerate()`.
- `break` skips the loop `else`, which makes the for-else useful for search patterns (Exercise 4).
- `range(a, b)` excludes `b`, `randint(a, b)` includes it.
- `print(..., end="")` keeps output on one line, a bare `print()` ends it.
- Never build a nested list with `[[0] * n] * m`, all rows would be the same object.
