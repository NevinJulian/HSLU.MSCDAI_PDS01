# SW06 · OOP Part I

**Date:** 2026-10-22
**Slides:** `sw06_oop_i.pdf` (dated 20 Oct 2026) · **Exercises:** [SW06 exercise sheet](sw06_exercises.md)

Topics: what object-oriented programming is, classes and objects, class syntax, class and object attributes, `self` and `cls`, printing an object with `__str__()`.

## Contents

1. [What is OOP](#1-what-is-oop)
2. [Classes and objects](#2-classes-and-objects)
3. [Class syntax: components](#3-class-syntax-components)
4. [Class header and documentation](#4-class-header-and-documentation)
5. [Class variables](#5-class-variables)
6. [Constructor](#6-constructor)
7. [Object variables](#7-object-variables)
8. [Object, class and static methods](#8-object-class-and-static-methods)
9. [Everything is an object](#9-everything-is-an-object)
10. [self and cls](#10-self-and-cls)
11. [Attribute call](#11-attribute-call)
12. [Printing an object: __str__()](#12-printing-an-object-__str__)

---

## 1. What is OOP

In contrast to functional programming, object-oriented programming is an alternative paradigm for better code structure and visibility. It primarily focuses on:

1. Ability to model complex real-world objects
2. Code maintainability
3. Code re-usability and modularisation, which is readability

The slides summarise it as:

- OOP is an advanced form of **encapsulation**, similar to functions. The abstraction paves the way for parallel computing and so enables handling complex and resource-intensive problems.
- All instructions are still executed **sequentially**.
- OOP provides an option to restrict and specify manipulation by accessing elements through **interfaces**.

### The box analogy

Object-oriented programming means:

- pack particular functions into a box
- and personalise the box with specific parameters

All boxes share the same toolbox and set of properties, but the property **values** are box specific, for example length and width. The box can be reproduced using assembly instructions.

```
Description:
  - length: 33cm
  - width: 27.2cm
  - height: 25cm
  - weight: 13.7kg
```

The analogy maps directly onto the vocabulary: the assembly instructions are the **class**, the produced boxes are the **objects**, the toolbox is the set of **methods**, and the description is the set of **attributes**.

**Note on the decorative code (slide 5).** The functions drawn inside the boxes are illustration, but one of them is wrong if copied:

```python
def mean_item(items):
    avg = 0
    for n, item in enumerate(items):
        avg += item
    else:
        return avg / n
```

`enumerate` counts from 0, so after the loop `n` is `len(items) - 1` and the function divides by one too few. For `[2, 4, 6, 8]` it returns 6.67 instead of 5.0, and a single-element list raises `ZeroDivisionError`. It should divide by `len(items)`. The `for ... else` is harmless but pointless here, since the `else` always runs when no `break` is involved.

## 2. Classes and objects

Assembly instructions for box construction are represented by the **class**. The produced boxes, all with the same set of tools but different property values, are called **objects**.

```python
class Package:

    package_nr = 0

    def __init__(self, length, width, height, weight):
        self.height = height
        self.width = width
        self.length = length
        self.weight = weight
        self.package_nr = Package.package_nr + 1
        Package.package_nr += 1

    def __str__(self):
        return f"Package number: {self.package_nr}"

    def get_weight(self):
        return self.weight
```

Generating a new object requires calling the class name and defining the specific properties by attributes passed to the constructor:

```python
my_package = Package(length=33, width=27.2, height=25, weight=13.7)

package_1 = Package(25, 25, 18, 9.7)
package_2 = Package(33, 19, 5, 3.2)
package_3 = Package(33, 19, 37, 13.7)
```

Each time a new object is generated, Python calls the constructor and passes the properties to the `__init__()` method as `__init__(length=33, width=27.2, height=25, weight=13.7)`.

Printing those three gives `Package number: 1`, `2`, `3`, and `Package.package_nr` ends at 3.

**Slide error (page 6).** The class in the picture on that slide ends the counter update with a bare name:

```python
self.package_nr = Package.package_nr + 1
package_nr += 1                            # UnboundLocalError
```

Assigning to `package_nr` inside the method makes it a **local** name for the whole method body, so `+= 1` tries to read a local that was never set. Running it raises:

```
UnboundLocalError: cannot access local variable 'package_nr' where it is not associated with a value
```

The same slide one page later ("Class Syntax: Components") has it right as `Package.package_nr += 1`, which is the version above. This is the same scope rule as the `global` keyword in [SW05](../sw05/sw05_functions_files.md#5-keyword-global): reading a name from an outer scope works, assigning to it makes it local.

## 3. Class syntax: components

In Python a class consists of a few elements:

| Element | Purpose |
|---|---|
| **header** with class name | Indicates the beginning of a class description |
| **`__init__()` method**, the constructor | Constructs a new object of the class |
| **variables** | *class*: belonging to the class description. *object*: belonging to a particular object |
| **methods** | *class*: provided by the class description. *object*: provided by the object |
| **`self` / `cls` parameter** | Reference to the object, required to access object attributes |

## 4. Class header and documentation

Like control structures and functions, a class is introduced by a header terminated with a colon. The header starts with the keyword `class`, followed by the class name and the colon.

```python
class Package:
    """
    This is the documentation of the
    class Package. It is not very short
    and spans multiple lines.
    """
```

- The header indent declares the block the class is visible in.
- The keyword must be lower case.
- Class names follow the **PascalCase** convention, each word beginning with a capital letter.
- When a class definition is entered, a **new namespace** is created.
- The class documentation directly follows the header and is a multi-line text block.

The docstring is not a comment. It is stored on the class and reachable at runtime as `Package.__doc__`, which is what `help(Package)` prints.

[Docs: class definition syntax](https://docs.python.org/3/tutorial/classes.html#class-definition-syntax)

## 5. Class variables

Class variables belong to a **class**. They are "global" variables storing information superior to all instances of a class.

A class variable:

- follows the naming convention of regular variables: `class_variable`
- is usually declared right after the class header: `class_variable = 'hello world'`
- requires no reference for declaration in the class
- is always called with the class reference: `Class.class_variable`
- can be created at runtime, without declaration in the class: `Class.class_variable = 66`

```python
class Package:
    """..."""
    package_nr = 0

    def __init__(self, length, width, height, weight):
        Package.package_nr += 1
```

A class variable exists once, no matter how many objects there are, which is what makes it work as a counter across all instances.

Worth knowing beyond the slide: an object can **read** a class variable through `self.package_nr`, but writing `self.package_nr = 5` does **not** change the class variable. It creates an object variable of the same name that shadows it from then on. That is exactly what the `Package` example above does on purpose: `self.package_nr` is this package's own number, `Package.package_nr` is the running total.

## 6. Constructor

The constructor, the `__init__()` method, is called by Python each time a new object is generated and defines the properties of the new object.

```python
package_1 = Package(25, 25, 18, 9.7)
```

The `__init__` method:

- is defined with the keyword `def` and terminated with a colon: `def __init__(self, param1, ...):`
- always has the name `__init__(...)`
- requires a reference to the object itself with the `self` parameter
- requires the `self` object reference always at the **first** position
- primarily defines the object properties, the object variables: `self.obj_var = 'hello world'`

`__init__` does not create the object, Python has already created it by the time `__init__` runs. It initialises it, which is why it returns nothing.

## 7. Object variables

Object variables belong to the **object** and define its properties.

An object variable:

- follows the naming convention of regular variables: `object_variable`
- is declared in the constructor or any other method
- always requires the object reference for declaration: `self.object_variable = 'hello world'`
- always requires the object reference for the call: `self.object_variable` inside the class, `object.object_variable` outside
- can be created at runtime, without declaration in the class: `object.object_variable = 66`

The last point is worth pausing on. Python lets you attach a new attribute to an object at any time, which is flexible and also means a typo such as `p.wieght = 5` silently creates a second attribute instead of raising an error. Declare everything an object needs in `__init__`.

## 8. Object, class and static methods

Python provides three different types of methods:

| | Object methods | Class methods | Static methods |
|---|---|---|---|
| Belong to | A particular object | A particular class | Neither object nor class |
| Purpose | Modifying the object's state | Modifying the class' state | Operations independent of any object or class state |
| First parameter | `self` | `cls` | none |
| Decorator | none | `@classmethod` | `@staticmethod` |

```python
class Package:
    package_nr = 0

    def __init__(self, weight):
        self.weight = weight
        Package.package_nr += 1

    def get_weight(self):
        return self.weight

    @classmethod
    def reset_instances(cls):
        cls.package_nr = 0

    @staticmethod
    def upper_case(name):
        return name.upper()
```

A static method is "fully functional": the return relies only on the input parameters. It sits inside the class purely because it belongs there thematically.

## 9. Everything is an object

In Python, everything is an object and variables hold **references** to these objects. Assigning an object to a variable creates a reference to that object in memory. Consequently all data types including `str`, `int`, `float` and `list` are objects.

```python
x = 99            # object of class int
s = 'hello world' # object of class str
li = [1, 2, 3, 4] # object of class list
```

By assigning a value to a variable, Python implicitly creates a new object with this value.

Objects and classes have their own namespace. Attributes of a namespace are accessed by the **dot notation**:

```python
object.attribute   # accessing an attribute of an object
Class.attribute    # accessing an attribute of a class
```

This is the same reference model as the mutable-argument warning in [SW05](../sw05/sw05_functions_files.md#3-mutable-data-types-in-functions). Two names can point at the same object, which is why mutating through one is visible through the other.

## 10. self and cls

The `self` and `cls` parameters refer to the **object** and the **class** respectively that the call belongs to, which allows calling or applying a variable or method of a particular object or class.

1. An object method, including `__init__()`, always requires a reference to the object by the parameter `self`:
   `def my_obj_fun(self, *param1, param2, param3)`
2. In an object method, object variables are always referred to by `self`:
   `self.my_obj_var = "hello world"`
3. A class method always requires a reference to the class by the parameter `cls`:
   `def my_class_fun(cls, *cparam1, cparam2, cparam3)`
4. In a class method, class variables are always referred to by `cls`:
   `cls.my_class_var = "hello world"`

**`self` and `cls` are not keywords** and can be any word. But the parameter itself is a must-have.

That is true but do not act on it. Every Python codebase and every linter expects `self` and `cls`, so renaming them only makes the code harder to read.

## 11. Attribute call

Calling an object or class method always requires a reference. As long as the method is called by addressing the object or class, Python implicitly passes the reference to the parameter list.

**Object method**

```python
def obj_method(self, *param1, param2, param3=True)
```

| Call | Form |
|---|---|
| Class intern | `self.obj_method(1, 2, 3, 4)` |
| By object | `object.obj_method(1, 2, 3, 4)` |
| By class | `Class.obj_method(object, 1, 2, 3, 4)` |

The last one is the one that shows what is really happening: `object.obj_method(...)` is shorthand for `Class.obj_method(object, ...)`. The object is passed as the first argument either way, it is just usually filled in automatically.

**Class method**

```python
@classmethod
def cls_method(cls, *param1, param2, param3=True)
```

| Call | Form |
|---|---|
| By class | `Class.cls_method(1, 2, 3, 4)` |
| By object | `object.cls_method(1, 2, 3, 4)` |

**Slide error (Attribute Call slide).** The slide gives the call by object as `object.cls_method(ClassName, 1, 2, 3, 4)`. That raises a `TypeError`:

```
TypeError: C.cls_method() takes 3 positional arguments but 4 were given
```

A `@classmethod` is bound to the class **whichever way you reach it**. Calling it through an instance already supplies `cls` automatically, so passing the class name again adds an extra positional argument. The correct form is `object.cls_method(1, 2, 3, 4)`.

The asymmetry with the object-method table is the point: for an object method you can pass the instance explicitly when you go through the class, because nothing is bound. For a class method the binding happens either way, so you never pass `cls` yourself.

## 12. Printing an object: `__str__()`

Printing a string to the console is intuitive, but what about objects?

- Why is a number printed when an `int` is passed to `print`?
- Why is `True` or `False` printed for a boolean?
- Why is `range(x, y)` printed for a range object?
- Why is something like the object location printed for an object such as `iter`?

Because `print` calls the object method `__str__()` and expects a `str` object that it prints to the console.

Consequently, by implementing a `__str__()` method, the programmer can define what is printed when an object of their own class is passed to `print`.

```python
def __str__(self):
    return 'object name'
```

Without one, you get the default inherited from `object`:

```
<__main__.NoStr object at 0x7e3f...>
```

Two rules worth remembering: `__str__` must **return** a string, not print it, and returning anything else raises a `TypeError`. The related `__repr__` is what the interactive interpreter and containers show, so printing a *list* of objects uses `__repr__`, not `__str__`. Implementing only `__str__` leaves `print([obj1, obj2])` showing memory addresses.

This is what [Exercise 1a](sw06_exercises.md#exercise-1-animals) is about: the snippet on the sheet ends in `print(obj)`, so the method to add is `__str__`.
