# Object id's
x = 2
y = x
print(id(x))
print(id(y))

a = [1,2]
b = a

print(id(a))
print(id(b))

# Copies and References
x = 2
y = x
x = 3
print(y) # -> ? 

a = [1,2]
print(a)
print(id(a))
b = a
a[1] = 99
print(a)
print(id(a))
print(a)
print(b) # -> ? 
