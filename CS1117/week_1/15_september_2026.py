"""

############################
### Intro to Programming ###
############################

kloc - 1000 lines of code
Dev wiki (within dev team)- architectural diagrams, standards of code, etc

gross_salary - snake case
grossSalary  - Camel case
GrossSalary  - Pascal case

### PEP 8 - Style Guide for Python ###

variables/functions should be snake_case
class names should be in PascalCase

dont use numbers for first character (obvious)

#######################################

### Data Types ###

Numerical
- Int
- Float
String
Boolean
List
Tuple
Dictionary

"""

## Tutorial 1 for Wednesday 16th
## Yippee

print("\n\n")

fundName = "luca"
#print(fundName)

fundID = 12345
#print(fundID)

fundBalance = 2345.67
#print(fundBalance)

#print(int(fundBalance))

fundActive = True
#print(fundActive)

yes = "yes"

print(f"Fund Name: {fundName} | Fund Balance: {fundBalance} | Fund Active?: {fundActive} | Gay guys kissing? {yes}")

print("\n")

# Interesting different way of printing values oooo aaahh
print("The fund name is: {}, and the fund balance is: {}".format(fundName, fundBalance))


## average

age = [12,14]

average_age = sum(age)/len(age)

print(f"The average age is {int(average_age)}")

#set_numbers = list(input("Enter here for samuel joseph gaynor : "))

#print(set_numbers)
#print(type(set_numbers))

## Dev practice - write a program to get area of rectangle based on length and width

# 1) Break down problem
# 2) Pseudocode
# 3) Use pseudocode to write python

## Pseudocode
# ask for length
# ask for width
# calculate with l*w
# print result
# ez dub

height = int(input("Enter height: "))
width  = int(input("Enter width: "))

area = width*height

print(f"The total area of your rectangle is {area}")