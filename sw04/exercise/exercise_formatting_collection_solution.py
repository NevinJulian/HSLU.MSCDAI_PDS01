
# Exercise Collection String Formatting - Solution

#%% Exercise 01
'''
Use the f"XXX" syntax to produce the following print out:
Hello Andreas and Ramon!

based on the given varibles.
'''

var1 = "and"
var2 = "Andreas"
var3 = "!"
var4 = "Dear Hello"
var5 = "Ramona"

print(f"{var4[5:]} {var2} {var1} {var5[:5]}{var3}")

#%% Exercise 02

'''
Use the "XXX".format() syntax to produce the following print out:
"My name is Giacomo, I am 10 years old, and I live in Padova."
based on the given dictionary. In the formatting call use:
1) order based
2) numbering based
3) key word based
4) dictionary key based
versions to insert the variables.
'''

insert_dict = {'name':'Giacomo', 'age':'10', 'city':'Padova'}

#1)
print("My name is {}, I am {} years old, and I live in {}.".format(insert_dict['name'], insert_dict['age'], insert_dict['city']))

#2)
print("My name is {0}, I am {1} years old, and I live in {2}.".format(insert_dict['name'], insert_dict['age'], insert_dict['city']))

#3)
print("My name is {name}, I am {age} years old, and I live in {city}.".format(name=insert_dict['name'], age=insert_dict['age'], city=insert_dict['city']))

#4)
print("My name is {0[name]}, I am {0[age]} years old, and I live in {0[city]}.".format(insert_dict))

#%% Exercise 03
'''
You are given list of n (even) numbers.
Write a program that prints for each pair [(first, last), (second, second last ), etc...] the following string:
X times Y is: X*Y
Use in place calculations to calculate the product directly in the string within the print statement.
'''

number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for ind,elem in enumerate(number_list):
    if ind+1 > len(number_list)/2:
        break
    first = elem
    second = number_list[-(ind+1)]
    print(f"{first} times {second} is: {first * second}")

