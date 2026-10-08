## Lectures 4 (and 5?, could be part 2 later on)
## 9am Monday 21st Week 2:
## nothing

## 2pm Monday 21st Week 2:

"""
def celciusToFarenheit(tempC):
    tempF = (tempC*9/5) + 32 
    return tempF
    

celcius = float(input("Enter temp here: "))
fahrenheit = celciusToFarenheit(celcius)
print(f"The temperature in fahrenheit is {fahrenheit}")

if fahrenheit > 90:
    print("Its warm as a motherfucker out here")
elif fahrenheit < 30:
    print("Its cold as fuck G")
"""

"""
## Russian Roulette
import random


# Initial Variables
min = 0
max = 6
replay = True

while replay == True:
    # Spin Spin
    active_shell = random.randint(min,max)
    firing_pin   = random.randint(min,max)
    divine_intervention = random.randint(0,99999999)

    # If shell is hit but no divine intervention
    if active_shell == firing_pin and divine_intervention != 903242:
        print("GG chud, you lose")
        
    # If shell is hit but divine intervention occurs
    elif active_shell == firing_pin and divine_intervention == 903242:
        print("DIVINE INTERVENTION PRAISE THE HEAVENS")
        
    # Beginners Luck
    else:
        print("You live, damn")
    
    user_replay_ans = input("Reroll? (y/n) : ") or "y"
    if user_replay_ans.lower() == "y":
        continue
    elif user_replay_ans.lower() == "n":
        replay = False
"""
