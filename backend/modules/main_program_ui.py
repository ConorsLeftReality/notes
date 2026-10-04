def display_menu():
    print("\t"*10 + "MENU")

    MENU = [] # Establish list to input menu items
            
    with open("backend/data/main_program_menu_items.txt","r") as f:
        for line in f:
            if line.strip("\n") == "" or (line.strip(" "))[0] == "#":
                continue
            else:
                line = line.strip("\n")
                MENU.append(str(line))

    i = 1 # Menu Option Number
    for menu_option in MENU:
        if menu_option == MENU[-1]:
            print(f"({i}) {menu_option}")
        else:
            print(f"({i}) {menu_option}")
            i += 1
    
    return i
        
## -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def menu_choice():
    
    user_choice = input("Select an option >>> ")
    if user_choice.isnumeric():
        return user_choice
    else:
        return False