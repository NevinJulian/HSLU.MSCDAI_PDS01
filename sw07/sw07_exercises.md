# SW07 · Exercise sheet: OOP II

**Sheet:** `exercises.pdf` ("Exercise Sheet SW7") · **Theory:** [SW07 notes](sw07_oop_ii.md) · **Notebook:** [exercise/sw07_exercises.ipynb](exercise/sw07_exercises.ipynb)

Additional material: `animals.csv`, the same file as [SW06](../sw06/sw06_exercises.md), already in `exercise/`.

All solutions below were run on Python 3.13 against the real `animals.csv`. Solutions are collapsed, try the task first.

---

## Exercise 1: Animals with inheritance

### Part a)

Produce a class structure where `Dog`, `Cat` and `Snake` are implemented as child classes of a base class `Animal`. Create the object variables in the base class, along with a method `print_basic_information()`, which prints 'type' and 'name' to the console.

In each child class, use the base class constructor with `super` and add an additional method `speak`, specific to that child class. In each child class, add an additional method where you return the sum of the object variables 'age' and 'legs'.

For each element in `animals.csv`, create an object of the corresponding subclass, let it print basic information (method from `Animal`), let it speak (method from the child class) and get the sum of 'age' and 'legs' as a return value.

<details>
<summary>Solution</summary>

```python
class Animal:
    def __init__(self, animal_type, name, age, weight, legs):
        self.animal_type = animal_type
        self.name = name
        self.age = age
        self.weight = weight
        self.legs = legs

    def print_basic_information(self):
        print(f"type: {self.animal_type}, name: {self.name}")


class Dog(Animal):
    def __init__(self, animal_type, name, age, weight, legs):
        super().__init__(animal_type, name, age, weight, legs)

    def speak(self):
        print(f"{self.name} says: Woof!")

    def sum_of_age_and_legs(self):
        return self.age + self.legs


class Cat(Animal):
    def __init__(self, animal_type, name, age, weight, legs):
        super().__init__(animal_type, name, age, weight, legs)

    def speak(self):
        print(f"{self.name} says: Meow!")

    def sum_of_age_and_legs(self):
        return self.age + self.legs


class Snake(Animal):
    def __init__(self, animal_type, name, age, weight, legs):
        super().__init__(animal_type, name, age, weight, legs)

    def speak(self):
        print(f"{self.name} says: Hiss!")

    def sum_of_age_and_legs(self):
        return self.age + self.legs
```

and the file loop from the sheet, with the branch filled in:

```python
obj_list = []
with open('./animals.csv') as f:
    for line in f.readlines()[1:]:
        animal_type = line.split(", ")[0]
        name = line.split(", ")[1]
        age = int(line.split(", ")[2])
        weight = int(line.split(", ")[3])
        legs = int(line.split(", ")[4])
        if animal_type == "dog":
            obj = Dog(animal_type, name, age, weight, legs)
        elif animal_type == "cat":
            obj = Cat(animal_type, name, age, weight, legs)
        elif animal_type == "snake":
            obj = Snake(animal_type, name, age, weight, legs)
        obj_list.append(obj)

for elem in obj_list:
    print("--\n")
    elem.print_basic_information()
    elem.speak()
    c_sum = elem.sum_of_age_and_legs()
    print(c_sum)
```

Output, first three of eleven:

```
--

type: dog, name: bello
bello says: Woof!
14
--

type: snake, name: masha
masha says: Hiss!
12
--

type: dog, name: wuffi
wuffi says: Woof!
12
```

**What changed against [SW06](../sw06/sw06_exercises.md#part-b).** There the three classes were unrelated and each repeated the full `__init__`. Here `__init__` lives once in `Animal` and each child forwards to it with `super()`, so adding a `legs` field is one edit instead of three.

**Two things in the sheet's template to watch:**

- It writes `class Cat():` and `class Snake():` with empty parentheses. That inherits from `object`, not from `Animal`. Only `Dog` has the `...FILL HERE...` placeholder in its header, so it is easy to leave the other two unparented and then wonder why `print_basic_information` is missing.
- The placeholder in the base class body is written `% ...FILL HERE...`. `%` is not a Python comment, that is a stray LaTeX comment marker from the sheet. Use `#`.

**On `print_basic_information`.** It prints, so it returns `None`. `sum_of_age_and_legs` returns, so the caller prints it. That split is the same one as in [SW06](../sw06/sw06_exercises.md#part-b), and the sheet's own driver loop relies on it: it calls the first two bare and wraps the third in `print`.

</details>

### Part b)

Often there are many different solutions to a particular task. Ideas like code readability and avoiding code duplication become more important in more complex applications. Do you find a way to reduce code duplication in the structure of part a)?

<details>
<summary>Solution</summary>

Part a) still has three kinds of duplication. Look at what actually differs between the three children: only the sound.

| Repeated in all three | Why it can move up |
|---|---|
| `__init__` that only calls `super()` | A child that adds nothing needs no constructor at all. Python inherits the parent's |
| `sum_of_age_and_legs` | It touches only `self.age` and `self.legs`, both defined in `Animal`. Nothing about it is dog-, cat- or snake-specific |
| `speak`, apart from one word | The structure is identical, only the sound differs. A class variable holds the difference |

```python
class Animal:
    sound = "..."

    def __init__(self, animal_type, name, age, weight, legs):
        self.animal_type = animal_type
        self.name = name
        self.age = age
        self.weight = weight
        self.legs = legs

    def print_basic_information(self):
        print(f"type: {self.animal_type}, name: {self.name}")

    def speak(self):
        print(f"{self.name} says: {self.sound}")

    def sum_of_age_and_legs(self):
        return self.age + self.legs


class Dog(Animal):
    sound = "Woof!"


class Cat(Animal):
    sound = "Meow!"


class Snake(Animal):
    sound = "Hiss!"
```

Three classes, one line each, and the output is identical to part a). Verified against all eleven rows.

**Why `self.sound` finds the child's value.** `sound` is a [class variable](../sw06/sw06_oop_i.md#5-class-variables). Looking up `self.sound` searches the object first, then its class, then the parents, so `Dog.sound` shadows `Animal.sound` for a `Dog`. The base class defines the fallback `"..."` so an `Animal` with no sound set still works rather than raising.

**The dispatch loop can lose its if-chain too.** A dictionary from the CSV's type string to the class removes the three branches:

```python
classes = {"dog": Dog, "cat": Cat, "snake": Snake}

obj_list = []
with open('./animals.csv') as f:
    for line in f.readlines()[1:]:
        animal_type, name, age, weight, legs = line.strip().split(", ")
        cls = classes[animal_type]
        obj_list.append(cls(animal_type, name, int(age), int(weight), int(legs)))
```

Classes are objects in Python, so they can sit in a dictionary and be called like any other callable. Adding a `Bird` is then one class and one dictionary entry, with no `elif` to extend.

**Where to stop.** Pushing everything into the base class is not automatically better. The rule worth carrying: move something up when it is genuinely shared, keep it down when it is genuinely specific. `speak` is shared in structure and specific in content, which is exactly what a class variable plus one inherited method expresses.

</details>

### Part c)

Override the `print_basic_information()` method in the child class `Dog` by using the class name as a parameter instead of `self.animal_type`. You can access the name of the class by `self.__class__.__name__`.

<details>
<summary>Solution</summary>

```python
class Dog(Animal):
    sound = "Woof!"

    def print_basic_information(self):
        print(f"type: {self.__class__.__name__}, name: {self.name}")
```

```
type: Dog, name: bello
bello says: Woof!
```

Against part a)'s `type: dog, name: bello`. Two differences worth noticing:

- **The capitalisation changes.** `animal_type` comes from the CSV as `"dog"`, the class is named `Dog`. The data and the class name are two separate sources of truth, which is the point of the exercise: the class already knows what it is, so the string field is redundant.
- **The `animal_type` field is still there** and still says `"dog"`. Overriding the method changed what is printed, not what is stored.

**Why `self.__class__.__name__` and not `Animal`.** This is the override lookup from the [notes](sw07_oop_ii.md#3-override) in action. `self.__class__` is the **actual** class of the object, so if you later write `class Puppy(Dog)` and call the inherited method, it prints `Puppy`, not `Dog`. Hard-coding the name would not do that.

`type(self).__name__` gives the same string and is the more usual spelling in modern code. The sheet asks for `self.__class__.__name__`, so use that.

**Where this leads.** Putting the override in `Animal` instead of `Dog` would let every subclass report its own name and make the `animal_type` constructor parameter unnecessary altogether. The exercise deliberately puts it only in `Dog` so you can see the two formats side by side in one run.

</details>

---

## Notes for the exam

- `class Child(Parent):` in the header, `super().__init__(...)` in the constructor. Forgetting the second leaves the parent's attributes unset and fails later with `AttributeError`.
- `super()` takes no `self`, `Parent.method(self, ...)` does.
- Python looks in the object's own class first, then up the chain. That is all overriding is.
- Every class inherits from `object`, which is where the default `__str__` comes from.
- `isinstance(x, Animal)` is True for a `Dog`, `type(x) == Animal` is not.
- A single underscore is convention. A double underscore is name mangling: `self.__x` inside `Demo` becomes `_Demo__x`, so a subclass asking for `self.__x` asks for a different attribute.
- An MRO inconsistency is raised at class definition time, not at call time.
