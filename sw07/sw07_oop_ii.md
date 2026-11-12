# SW07 · OOP Part II

**Date:** 2026-10-29, onsite
**Slides:** `sw07_oop_ii.pdf` (dated 27 Oct 2026) · **Exercises:** [SW07 exercise sheet](sw07_exercises.md)

Topics: inheritance, the class `object`, overriding, multiple inheritance, the method resolution order, access modifiers.

## Contents

1. [What is inheritance](#1-what-is-inheritance)
2. [What a child class gets](#2-what-a-child-class-gets)
3. [Override](#3-override)
4. [The class object](#4-the-class-object)
5. [Syntax](#5-syntax)
6. [Multiple inheritance: concept](#6-multiple-inheritance-concept)
7. [MRO: the problem](#7-mro-the-problem)
8. [MRO: the rules](#8-mro-the-rules)
9. [Access modifiers](#9-access-modifiers)

---

## 1. What is inheritance

Inheritance creates a **hierarchy of classes**:

- from a base class `Animal` with basic commonalities,
- go to more specific groups like `Bird` or `Cow`.

```
          Animal          Parent, Super or Base Class
         ╱      ╲
      Bird      Cow       Child, Sub or Derived Class
```

Objectives of inheritance:

- avoid code duplication, that is, reuse code
- increase maintainability

Two built-in functions identify the class of an object:

| Function | True when |
|---|---|
| `isinstance(object, classinfo)` | object is an instance of `classinfo` or of a subclass of it |
| `issubclass(class, classinfo)` | class is a subclass of `classinfo` |

`isinstance` is the one to reach for. `type(x) == Animal` is False for a `Dog`, while `isinstance(x, Animal)` is True, which is almost always what you meant.

This is the answer to the duplication problem from [SW06](../sw06/sw06_exercises.md#part-b), where `Dog`, `Cat` and `Snake` each carried a byte-identical `__init__`.

## 2. What a child class gets

Child classes get all properties (attributes) from the parent class. Class or object variables **and** methods defined in the parent class `Animal` also hold in the child classes `Bird` and `Cow`.

In this way, common or similar attributes only need to be defined and maintained in the parent class:

- Size of the full application gets reduced
- Easy to add new subgroups
- Simple debugging and maintenance
- Simple to extend functionality

Typically, child classes **extend** parent classes.

## 3. Override

In some cases child classes do not totally match the parent class attributes and require different method behaviour. A child class can then **override** variables or methods from the parent class, under exactly the same name.

This allows you to:

- extend methods with additional functionality, or
- completely substitute the behaviour of the parent method

**When a method of an object is called, Python always seeks the method in the class of the object first, before seeking in the parent class.** This also holds for methods such as `__str__()`.

That lookup order is the whole mechanism. There is nothing special about overriding, it is just the first match along the chain winning, and [the MRO](#8-mro-the-rules) is the precise statement of what that chain is.

## 4. The class `object`

In Python the class `object` provides basic functionalities, and **each class except `object` itself inherits from it**.

```
class object
 |  The base class of the class hierarchy.
 |
 |  When called, it accepts no arguments and returns a new featureless
 |  instance that has no instance attributes and cannot be given any.
```

So `class Animal:` and `class Animal(object):` are the same thing, and every class already has `__str__`, `__repr__`, `__eq__` and the rest before you write a line. The default `<__main__.Animal object at 0x...>` from [SW06](../sw06/sw06_oop_i.md#12-printing-an-object-__str__) is `object.__str__` doing its job.

Docs: [object](https://docs.python.org/3/library/functions.html#object)

## 5. Syntax

Similar to a function or method, a class is able to take over a parameter, the name of the parent class. When declaring a child class, the reference to the parent class has to be passed to the class header.

To inherit from the parent class `Animal`:

- the parent class `Animal` must be **declared before** referring to it
- the parent class name `Animal` has to be passed to the **child class header**
- the constructor of the child class must **call the constructor of the parent class** too

```python
class Animal:
    def __init__(self, weight):
        self.weight = weight

class Bird(Animal):
    def __init__(self, weight):
        super().__init__(weight)
        # or Animal.__init__(self, weight)
```

### Extending a parent method

When extending the functionality of a parent class by overriding a method, or in general to use the parent's methods, they can be referred to using `super()` or the parent's class name.

```python
class Animal:
    def __init__(self, weight):
        self.weight = weight

    def get_weight(self):
        return self.weight

class Bird(Animal):
    def __init__(self, weight):
        super().__init__(weight)
        # or Animal.__init__(self, weight)

    def get_weight(self):
        return super().get_weight() / 10
        # or return Animal.get_weight(self) / 10
```

`Bird(500).get_weight()` returns `50.0`, while `Animal.get_weight(bird)` still returns `500`.

`super()` returns a **proxy object** that delegates method calls to a parent or sibling class of type.

Two practical notes on the two spellings:

- `super().method(args)` takes no `self`, because the proxy already carries it. `Animal.method(self, args)` does, because you are calling the plain function off the class.
- Prefer `super()`. Hard-coding `Animal` breaks the moment the hierarchy changes, and in [multiple inheritance](#6-multiple-inheritance-concept) it skips the sibling classes that the MRO would otherwise visit. The word "sibling" in the slide's definition is exactly that case: `super()` does not simply mean "my parent", it means "the next class in the MRO".

**If you forget the `super().__init__()` call**, the parent's attributes are never assigned and every later use raises `AttributeError`. There is no warning, because Python does not call it for you.

Docs: [super](https://docs.python.org/3/library/functions.html#super)

## 6. Multiple inheritance: concept

A child class that inherits from a parent class inherits all attributes from all parent classes.

Three scenarios:

| Scenario | Shape |
|---|---|
| **Single inheritance** | One child class inherits from one parent class |
| **Multiple single inheritance** | Multiple child classes inherit from one and the same parent class |
| **Multiple inheritance** | One child class inherits from multiple parent classes |

Only the third causes the conflicts the rest of this section is about. The second is the ordinary `Dog`, `Cat`, `Snake` case from the exercise.

**Slide imprecision.** The slide says a child "inherits all except of `__private` attributes". Private attributes **are** inherited, the data is right there on the object. What stops you reaching them is [name mangling](#9-access-modifiers), not an inheritance rule: inside a subclass `self.__x` compiles to `self._Subclass__x`, while the value is stored under `_Parent__x`. The effect looks the same from the outside, but the reason matters when you go looking for the attribute in `vars(obj)` and find it sitting there.

## 7. MRO: the problem

Dealing with multiple inheritance causes conflicts in resolving referenced attributes, originating from multiple references to the same or overridden attributes inherited from multiple parent classes.

The slide's example, as a UML diagram:

```
                  Animal
                  weight: int
                  get_weight(): int
                 ╱              ╲
            extends            extends
               ╱                    ╲
   Bird                              Fish
   wing_size: int                    dive_depth: int
   fly(): None                       dive(): None
   get_weight(): int  ← overridden
               ╲                    ╱
            extends            extends
                 ╲              ╱
                  Penguin
                  fur_color: str
                  get_fur_color(): str
```

```python
my_penguin = Penguin()
print(my_penguin.get_weight())
```

Which `get_weight()` is called? Note from the diagram that only **Bird** overrides it. `Fish` has no `get_weight` of its own and simply inherits `Animal`'s. So the conflict is between Bird's version and Animal's original, reachable through Fish.

To solve these conflicts, Python introduced the **Method Resolution Order (MRO)** in version 2.3.

## 8. MRO: the rules

The MRO applies some rules and attempts to find a **linearization** of all classes. It starts at the root and finds linearizations `L(class)` for the more specialised classes:

```
L(Animal)  = Animal
L(Bird)    = Bird
L(Fish)    = Fish
L(Penguin) = Penguin + merge(Bird Animal, Fish Animal)
...
L(Penguin) = Penguin Bird Fish Animal
```

Verified in Python 3.13:

```python
>>> [c.__name__ for c in Penguin.__mro__]
['Penguin', 'Bird', 'Fish', 'Animal', 'object']
>>> Penguin().get_weight()
'Bird.get_weight'
```

So Bird's override wins, because Bird comes before Animal in the order. `object` always sits at the end, which the slide's shorthand leaves off.

The slide's `merge(...)` also leaves off one term. The full C3 rule is

```
L(C) = C + merge( L(B1), ..., L(Bn), [B1, ..., Bn] )
```

The trailing list of direct parents is what forces the declaration order to be respected, and it is exactly the term that makes the [inconsistency below](#when-no-linearization-exists) fail.

### Order of inheritance

The linearization process depends on the order of inheritance: `class Penguin(Bird, Fish)` against `class Penguin(Fish, Bird)`.

Worth being precise about what changes. Reversing the order does change the MRO:

```python
>>> [c.__name__ for c in PenguinRev.__mro__]
['PenguinRev', 'Fish', 'Bird', 'Animal', 'object']
```

but in this example it does **not** change which `get_weight` runs. It still resolves to Bird's, because `Fish` does not define one and the search falls through to the next class in the order. Order decides the answer only when more than one class in the chain actually defines the attribute.

### When no linearization exists

Trying to find a linearization for a given order of parent classes, the MRO does not always find a feasible solution. This case provokes an MRO inconsistency error:

```python
class A(): pass
class B(A): pass
class F(A): pass
class P(B, F): pass
class E(F, B): pass

class C(P, E): pass
```

```
TypeError: Cannot create a consistent method resolution order (MRO) for bases B, F
```

`P` demands B before F, `E` demands F before B, and `C` would need both at once. To solve this, classes B and F must have the **same inheritance order**:

```python
class P(B, F): pass
class E(B, F): pass
```

which gives `C2 → P2 → E2 → B → F → A → object`.

Note the error appears at **class definition time**, not when a method is called. Python builds the MRO as soon as it reads the `class` statement, so this fails on import rather than in production.

Docs: [The Python 2.3 Method Resolution Order](https://docs.python.org/3/howto/mro.html)

## 9. Access modifiers

For encapsulation purposes, declared variables and methods in a class can have three different states of visibility. The visibility defines what class attributes can be accessed:

1. from an object level (**public**)
2. in the declaration of a subclass (**protected**)
3. in the declaration of the own class only (**private**)

Since Python is a script language and does not compile code in advance of execution, it lacks keywords defining an attribute's accessibility. There is instead a **convention** in the naming of attributes, using `_` to signal access restrictions.

**But this is only a convention. Python has no hard restrictions and allows access to all attributes on object level.**

| Visibility | Naming | Access |
|---|---|---|
| **public** | regular name, no special characters | `self.public_attribute` or `object.public_attribute` |
| **protected** | one leading underscore `_` | `self._protected_attribute`, in the own class or a derived class |
| **private** | two leading underscores `__` | `self.__private_attribute`, in the own class only |

**Slide error (the private slide).** It says "**Protected** attributes are indicated with two leading underscore" and "**Protected** attributes can always be accessed by: `self.__private_attribute`". Both should read **Private**, copy-pasted from the protected slide one page earlier. Also two different slides in the deck carry the footer "Page 18", so page numbers are not a reliable way to refer to this section.

### The convention is only half the story

The single underscore really is pure convention. Python does nothing with it, it is a note to the next developer.

The double underscore is not. Python rewrites the name, which is called **name mangling**: inside class `Demo`, `self.__private` is compiled to `self._Demo__private`.

```python
>>> d = Demo()
>>> d.__private
AttributeError: 'Demo' object has no attribute '__private'
>>> d._Demo__private
3
>>> [k for k in vars(d)]
['public', '_protected', '_Demo__private']
```

So the attribute is reachable, exactly as the slide says, but only under its mangled name. The attribute is not hidden, it is **renamed**.

This also explains the subclass behaviour:

```python
class Sub(Demo):
    def try_private(self):
        return self.__private      # compiles to self._Sub__private

>>> Sub().try_private()
AttributeError: 'Sub' object has no attribute '_Sub__private'
```

The subclass fails not because access was denied but because it asked for a differently named attribute. The parent's value is still sitting on the object as `_Demo__private`.

The practical consequence: use a single underscore for "internal, do not rely on this". Reach for the double underscore only when you actually want to avoid a name collision in a subclass, which is the problem it was designed for.
