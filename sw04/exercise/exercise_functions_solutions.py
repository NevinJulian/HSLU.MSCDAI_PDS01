# Exercise Solutions Functions


#%% Exercise 01
def is_even_num(l):
    enum = []
    for n in l:
        if n % 2 == 0:
            enum.append(n)
    return enum

print( is_even_num( [1, 2, 3, 4, 5, 6, 7, 8, 9] ) )


#%% Exercise 02
def unique_list(a_list):
    result = []
    for element in a_list:
        if element not in result:
            result.append(element)
    return result

print(unique_list([1, 2, 3, 3, 3, 3, 4, 5]))
print(set([1, 2, 3, 3, 3, 3, 4, 5]))


#%% Exercise 03
# This function adds two numbers
def add(x, y):
   return x + y

# This function subtracts two numbers
def subtract(x, y):
   return x - y

# This function multiplies two numbers
def multiply(x, y):
   return x * y

# This function divides two numbers
def divide(x, y):
   return x / y
 
def main():
    print("Select operation.")
    print("1.Add")
    print("2.Subtract")
    print("3.Multiply")
    print("4.Divide")

    # Take input from the user
    choice = input("Enter choice(1/2/3/4):")

    num1 = int(input("Enter first number: "))
    num2 = int(input("Enter second number: "))

    if choice == '1':
       print(num1,"+",num2,"=", add(num1,num2))

    elif choice == '2':
       print(num1,"-",num2,"=", subtract(num1,num2))

    elif choice == '3':
       print(num1,"*",num2,"=", multiply(num1,num2))

    elif choice == '4':
       print(num1,"/",num2,"=", divide(num1,num2))
    else:
       print("Invalid input")

main()


#%% Exercise 04
def circumference(length=2, width=1):
    return 2 * (length + width)

c1 = circumference(width=2)          # 2 should be the width !!!
print(c1)

# or with length 5 and width 3:
c2 = circumference(length=5, width=3)
print(c2)

# how could the function also have been called
# with length 5 and width 3
c3 = circumference(5, 3)
print(c3)

# you can even change the order of keyword parameters
# try it: Change the order of  parameters!
c4 = circumference(width=3, length=5)    # keyword parameter order swapped!
print(c4)


#%% Exercise 05
# Example 1: 
def hello(name="Nameless"):
    print("Hello " + name + "!")

hello("Peter")

# without parameters => the standard value is used!
hello()


# Example 2:
def circumference(laenge=2, breite=1):
    return 2 * (laenge + breite)

c1 = circumference(5, 3)
print(c1)

# for the width the standard value "1" is used
c2 = circumference(5)
print(c2)

# Both standard values are now used
c3 = circumference()
print(c3)