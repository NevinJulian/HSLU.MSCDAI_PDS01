'''
Exercise Modules

Fill the parts indicated by "...FILL HERE..." such that the code becomes executable and matches the OUT: statements.

'''

#%% Import entire module: string_operations.py
import string_operations as SO

print(SO.__doc__)
#OUT: Collection of methods to manipulate strings.

SO.say_something()
#OUT: Hello

print(SO.module_variable)
#OUT: Hello

my_string = "Hello Universe!"
rev = SO.reverse(my_string)
print(rev)
#OUT: !esrevinU olleH

bi_rev = SO.bi_rev(my_string)
print(bi_rev)
#OUT: !seiUolH

#%% Import specific functions only
from string_operations import reverse
print(reverse("!esrevinU olleH"))
#OUT: Hello Universe!

# greet somebody in reversed order
from string_operations import greet_somebody
name = 'Andreas'
print(greet_somebody(reverse(name)))
#OUT: Hello saerdnA

