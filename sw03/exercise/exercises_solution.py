###################
# Exercise 1
###################
"""
Write a python program that constructs the following pattern using a nested for loop:

*
**
***
****
*****
****
***
**
*
"""

n = 5
for i in range(n):
    for j in range(i):
        print("* ", end="")
    print("")

for i in range(n,0,-1):
    for j in range(i):
        print("* ", end="")
    print("")



###################
# Exercise 2
###################
"""
Write a python program to count the number of even and odd numbers contained in a sequence of numbers.
Example:
numbers = (1,2,3,4,5,6,7,8,9,10)
Output:
Number of even numbers: 5
Number of odd numbers: 5
"""

num_seq =[1,2,3,4,5]
even_counter = 0
odd_counter = 0

for elem in num_seq:
    if elem%2==0:
        even_counter = even_counter + 1
    else:
        odd_counter = odd_counter + 1

###################
# Exercise 3
###################
"""
Write a Python program which takes two digits m (row) and n (column) as input and
generates a two-dimensional structure (e.g. nested list). The value in the i-th row and j-th column 
should be i*j.
Note :
i = 0, 1, … , m-1
j = 0, 1, … , n-1
Input Test Data - Rows = 3
Input Test Data - Columns = 4
Expected Result: [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 4, 6]]
"""

row_num = int(input("Input Test Data - Rows = "))
col_num = int(input("Input Test Data - Columns: "))
# initialize the list with '0'
result_list = []
for row in range(row_num):
    inner_list = []
    for col in range(col_num):
        c_value = row * col
        inner_list.append(c_value)
    result_list.append(inner_list)
print(result_list)

###################
# Exercise 4
###################
"""
Write a Python program to find all numbers between 200 and 500 (limits included) only containing even digits.
Correct solution: 
200,202,204,206,208,220,222,224,226,228,240,242,244,246,248,260,262,264,266,26
8,280,282,284,286,288,400,402,404,406,408,420,422,424,426,428,440,442,444,446,
448,460,462,464,466,468,480,482,484,486,488
"""
candidates = range(200,501)
result = []

for number in candidates:
    str_cand = str(number)
    for elem in str_cand:
        digit = int(elem)
        if digit%2 == 0:
            continue
        else:
            break
    else:
        result.append(int(str_cand))
        
###################
# Exercise 5
###################
"""
Write a Python program to guess a number between 1 to 10. You can use the predefined code block to create a random number or just set it manually. Next, the user is prompted to enter a guess. If the guess is wrong, a message "to big" or "to small" is printed to the console and the prompt (user input) appears again until the guess is correct. If the guess is correct, "Well guessed!" will be printed and the program ends.

Extension:
The number of trials should be prompted as well: "Well done - you have tried it 4 times!"
"""

# Code block to create a random number
from random import randint
random_number = randint(1,10)
# End code block to create a random number

guess_num = int(input("Guess a number between 1 and 10:"))
number_of_guesses = 1
while random_number != guess_num:
    if random_number > guess_num:
        print("the number is too small")
    else: 
        print("the number is too big")
    guess_num = int(input("Next try:"))
    number_of_guesses = number_of_guesses + 1
print("Well guessed: the random number was correct!")
print("It took you:", number_of_guesses, " guesses.")


###################
# Exercise 6
###################
"""
Suppose we want to draw a Christmas tree like the following:
     x
    xxx
   xxxxx
  xxxxxxx
 xxxxxxxxx
xxxxxxxxxxx
    xxx
    xxx

Create a program that asks the user for the trunk-excluded-height of the Christmas tree and then draws the tree according to these rules:

 - The height of the trunk is always 2
 - The width of the trunk 3 in case the entire height is $>$ 5 or 1 in case the entire height is $<=$ 5
"""
 
height = int(input("What is the height of your tree?:"))
if height > 5:
    chunk_width = 3
else:
    chunk_width = 1

# head
for row in range(height):
    for elem in range(height-row):
        print(" ", end="")
    print("*"*(row+1) + "*"*(row))
# trunk
for elem in range(2):
    if chunk_width == 3:
        print(" "*(height-1),end="")
        print("*"*chunk_width)
    else:
        print(" "*height,end="")
        print("*")
    
