# SW06 · Exercise sheet: OOP

**Sheet:** `exercises.pdf` ("Exercise Sheet SW6") · **Theory:** [SW06 notes](sw06_oop_i.md) · **Notebook:** [sw06_exercises.ipynb](sw06_exercises.ipynb)

Additional material: `animals.csv`, from ILIAS and also in this folder.

All solutions below were run on Python 3.13 against the real `animals.csv`. Solutions are collapsed, try the task first.

---

## Exercise 1: Animals

### Part a)

For each animal in the file (rows), print:

```
Hi, I'm a {animal_type} and my name is {name}!
```

Solve the exercise by writing a class `Animal` and adding a method allowing to print the requested string. For this task it is not necessary to differentiate between animal types.

Template from the sheet:

```python
class FillHere:

    def __init__(self, animal_type, name, age, weight, legs):
        self.animal_type = animal_type
        self.name = name
        self.age = age
        self.weight = weight
        self.legs = legs

    # ...FILL HERE...

with open('./animals.csv') as f:
    for line in f.readlines()[1:]:
        animal_type = line.split(", ")[0]
        name = line.split(", ")[1]
        age = int(line.split(", ")[2])
        weight = int(line.split(", ")[3])
        legs = int(line.split(", ")[4])
        #create objects
        obj = Animal(animal_type, name, age, weight, legs)
        print(obj)
```

<details>
<summary>Solution</summary>

The loop ends in `print(obj)`, so the method to add is `__str__`. That is the whole point of the last section of the lecture: `print` calls `__str__()` on the object and prints whatever string it returns.

```python
class Animal:
    def __init__(self, animal_type, name, age, weight, legs):
        self.animal_type = animal_type
        self.name = name
        self.age = age
        self.weight = weight
        self.legs = legs

    def __str__(self):
        return f"Hi, I'm a {self.animal_type} and my name is {self.name}!"
```

Output, all 11 rows:

```
Hi, I'm a dog and my name is bello!
Hi, I'm a snake and my name is masha!
Hi, I'm a dog and my name is wuffi!
Hi, I'm a cat and my name is leslie!
Hi, I'm a cat and my name is dummy!
Hi, I'm a cat and my name is puffy!
Hi, I'm a snake and my name is snizzy!
Hi, I'm a snake and my name is sazzles!
Hi, I'm a dog and my name is buddy!
Hi, I'm a cat and my name is wooly!
Hi, I'm a cat and my name is beast!
```

**Note the template names the class `FillHere` but instantiates `Animal`.** `FillHere` is a placeholder, name the class `Animal`.

**Two details in the parsing loop worth understanding, since you did not write it:**

- `f.readlines()[1:]` skips the header row `animal_type, name, age, weight, legs`.
- The split is on `", "`, comma **and** space, which is what the file uses. The last field comes out as `'4\n'` with the newline still attached, but `int('4\n')` is 4 because `int()` strips surrounding whitespace. It works by luck rather than by design: the same code would break if `legs` were the `name` column, since `str` keeps the newline.

Calling `line.split(", ")` five separate times splits the same string five times. Doing it once is cheaper and reads better:

```python
animal_type, name, age, weight, legs = line.strip().split(", ")
obj = Animal(animal_type, name, int(age), int(weight), int(legs))
```

</details>

### Part b)

Now we are interested in the various sounds the animal types make. Write a separate class for each animal type. Provide a method `speak`, which depending on the animal type prints different sounds.

The sheet gives `Dog`, `Cat` and `Snake` skeletons plus a loop that builds `obj_list` and ends with:

```python
for elem in obj_list:
    elem.speak()
```

<details>
<summary>Solution</summary>

```python
class Dog:
    def __init__(self, name, age, weight, legs):
        self.name = name
        self.age = age
        self.weight = weight
        self.legs = legs

    def speak(self):
        print(f"{self.name} says: Woof!")


class Cat:
    def __init__(self, name, age, weight, legs):
        self.name = name
        self.age = age
        self.weight = weight
        self.legs = legs

    def speak(self):
        print(f"{self.name} says: Meow!")


class Snake:
    def __init__(self, name, age, weight, legs):
        self.name = name
        self.age = age
        self.weight = weight
        self.legs = legs

    def speak(self):
        print(f"{self.name} says: Hiss!")
```

Output:

```
bello says: Woof!
masha says: Hiss!
wuffi says: Woof!
leslie says: Meow!
dummy says: Meow!
puffy says: Meow!
snizzy says: Hiss!
sazzles says: Hiss!
buddy says: Woof!
wooly says: Meow!
beast says: Meow!
```

**`speak` prints, it does not return.** The sheet's loop is `elem.speak()` with no `print` around it, so the method has to do the printing itself. That is the opposite of part a), where `print(obj)` means `__str__` has to **return** a string. Mixing the two up is the usual mistake here: a `speak` that returns would print nothing, and a `__str__` that prints would print `None` on top.

**The loop works through duck typing.** `obj_list` holds three different types and `elem.speak()` never checks which. Python only cares that the method exists, which is why three unrelated classes can be driven by one loop.

**The duplication is the point.** All three `__init__` methods are identical, and only `speak` differs. That is exactly the problem inheritance solves, which is OOP part II next week. There an `Animal` base class holds `__init__` once and `Dog`, `Cat`, `Snake` override only `speak`.

</details>

## Exercise 2: Letters and digits

Write a Python program that asks for a string as input and calculates the number of digits and letters contained.

```
Input = "python 3.2"

Expected result:
Letters: 6
Digits: 2
```

Hint: check the documentation for `string.isdigit()` and `string.isalpha()`.
Comment: provide the solution method as part of a class.

<details>
<summary>Solution</summary>

```python
class StringCounter:
    def __init__(self, text):
        self.text = text

    def count(self):
        letters = 0
        digits = 0
        for char in self.text:
            if char.isalpha():
                letters += 1
            elif char.isdigit():
                digits += 1
        return letters, digits

    def report(self):
        letters, digits = self.count()
        print(f"Letters: {letters}")
        print(f"Digits: {digits}")


counter = StringCounter(input("Enter a string: "))
counter.report()
```

With `python 3.2` this prints `Letters: 6` and `Digits: 2`, matching the sheet. The space and the dot are neither, which is why the two counts do not add up to the length.

**Why a class at all.** The task is one loop, so the class adds nothing functionally. It is there to practise the shape: state in `__init__`, work in a method, and a second method that uses the first. Splitting `count` from `report` is worth keeping, since `count` returns data that something else can use while `report` only prints.

The counting itself is shorter as a comprehension, though the explicit loop is clearer while learning:

```python
letters = sum(1 for c in self.text if c.isalpha())
digits = sum(1 for c in self.text if c.isdigit())
```

**`elif` versus a second `if`.** No character is both a letter and a digit, so both work here. `elif` saves the second test.

**What these methods actually mean**, since they are Unicode-aware and not ASCII-only:

| Character | `isalpha()` | `isdigit()` |
|---|---|---|
| `a` | True | False |
| `ä` | **True** | False |
| `3` | False | True |
| `²` | False | **True** |
| `.` | False | False |
| space | False | False |

So accented letters count as letters, and a superscript `²` counts as a digit even though `int('²')` fails. Fine for this exercise, worth knowing before using `isdigit()` to validate numeric input.

</details>

---

## Notes for the exam

- `print(obj)` calls `__str__()`, which must **return** a string. A method called directly, like `speak()`, does its own printing.
- Without `__str__`, printing an object gives `<__main__.Animal object at 0x...>`.
- `__repr__`, not `__str__`, is what shows up when you print a list of objects.
- Class variable lives once on the class, object variable once per object. `self.x = 5` never writes to the class variable, it shadows it.
- `self` must be the first parameter of an object method, `cls` of a class method. Neither is a keyword, both are mandatory.
- `object.method(args)` is shorthand for `Class.method(object, args)`. A `@classmethod` binds the class either way, so you never pass it yourself.
- Assigning to a name inside a method makes it local for the whole method, which is what breaks a bare `counter += 1` on a class variable.
