########################
# SOLUTION 1: if, else, elif
########################

daynumber = int(input("Input the day of Week: (1 = Montag, 2 = Dienstag, ..., 7 = Sonntag) "))

# print(type(daynumber))
# print("daynumber:", daynumber)

if daynumber == 1:
    print("You have to work ...!")  
elif daynumber == 2:    
    print("You have to work ...!")
elif daynumber == 3:    
    print("You have to work ...!")            
elif daynumber == 4:    
    print("You have to work ...!")            
elif daynumber == 5:    
    print("You have to work ...!")            
elif daynumber == 6:    
    print("Enjoy the time now ...!")            
elif daynumber == 7:    
    print("Enjoy the time now ...!")           
else:
    print("Wrong input or do you live on another planet?")

########################
# Alternative Solution 1: if, else, elif
########################

daynumber = int(input("Input the day of Week: (1 = Montag, 2 = Dienstag, ..., 7 = Sonntag) "))

# print(type(daynumber))
# print("daynumber:", daynumber)

if daynumber in (1,2,3,4,5):
    print("You have to work ...!")
elif daynumber in (6,7):
    print("Enjoy the time now ...!")
else:
    print("No valid input...")

########################
# SOLUTION 2: if, else, elif
########################

age = int(input("Input the age of the custumer:  "))

if age >= 18 and age <25:
    print("The customer belongs to the 'Youth' category")
elif age >= 25 and age <35:
    print("The customer belongs to the 'YoungAdult' category")
elif age >= 35 and age <60:
    print("The customer belongs to the 'MiddleAged' category")
elif age >= 60 :
    print("The customer belongs to the 'Senior' category")

########################
# SOLUTION 3: if, else, elif
########################

scale = input("Put F for entering Fahrenheit, C for entering Celsius:")
if scale == 'F':
    T_F = float(input("Your number in Fahrenheit:"))
    T_C = (5/9) * (T_F - 32)
    print("Your number in °C: ")
    print(T_C)
elif scale == 'C':
    T_C = float(input("Your number in Celcius:"))
    T_F = T_C * (9/5) + 32
    print("Your number in °F: ")
    print(T_F)
else:
    print('Not a valid input!')

########################
# SOLUTION 4: if, else, elif
########################

a = int( input( "Input 'a': "))
b = int( input( "Input 'b': " ))
c = int( input( "Input 'c': " )) 

if a < b:
    if b < c:
        print(a,b,c)
    else:
        if a < c:
            print(a,c,b)
        else:
            print(c,a,b)
else:
    if b > c:
        print(c,b,a)
    else:
        if a > c:
            print(b,c,a)
        else:
            print(b,a,c)

########################
# SOLUTION 5: if, else, elif
########################

a=1
b=2
c=2

if (a>b or a<(b/2) or a+c>b ):
    print("condition fulfilled")

########################
# SOLUTION 6: if, else, elif
########################

a=5
b=5
c=2

if ((a//2)%2 != 0 or (b-c)%2 == 0 or (a != b) and (b != c)):
    print("condition fulfilled")
