## Main Program for working with this repository
## 
## Functions:
## Create New Lecture File
## Regenerate/generate Index file for a module
## Advanced Functions: 
##      Add module message for a module
##      Add/Remove Enrolled modules
##      Update Main Index Page

## ====================================================================
## ========================== IMPORT MODULES ==========================
## ====================================================================

import time # Sleep

## GENERATION MODULE    - Clear Screen, make directory (MKDIR), Generate Module Index Page (MODULE_INDEX_PAGE), 
##                        Generate Lecture File (LECTURE_FILE), Generate Main Index Page (MAIN_INDEX_PAGE)
##                      - USED TO GENERATE FILES OR DIRECTORIES
from modules.generate import make_directory,create_module_index_page_html,create_lecture_html_file


## DATA MANIPULATION MODULE - Collects user inputs about a lecture, resolves and creates a modules directory, Enrolled Module file updating, 
##                            Module Messages file updating
##                          - USED TO COLLECT, WORK WITH, AND MANIPULATE DATA
from modules.data_manipulator import lecture_information_collection,module_selection_resolver,week_selection_resolver
from modules.data_manipulator import write_lecture_notes_html,write_index_file_to_module,menu_choice_resolver #enrolled_modules_update, module_messages_update


## UTILITIES MODULE     - pause, clear screen
##                      - VARIOUS USES, READ module_documentation.txt in /backend
from modules.utilities import pause,clear_screen

## UTILITIES MODULE     - display menu,
##                      - User Interface, usually graphical functions
from modules.main_program_ui import display_menu, menu_choice

## ====================================================================
## ========================== IMPORT SCRIPTS ==========================
## ====================================================================

## LECTURE NOTES GENERATION SCRIPT  - lecture notes generation script
##                                  - Used to call the main script for lecture notes generation
from modules.lecture_note_generate import lecture_notes_generation_script


## TODO: Make the program regenerate/update all index files if asked to, as new modules wont be indexed if generated
## TODO: Make program update the main index page with new module folders, and have title for module too (in file)

## =======================================================================================
## ============================     MAIN CODE FOR PROGRAM    =============================
## =======================================================================================

program_banner = r"""
    b.                      
    88b                     ::::    :::  :::::::: ::::::::::: :::::::::: ::::::::        ::::::::   ::::::::  ::::    :::  ::::::::   ::::::::  :::        ::::::::::      
    888b.                   :+:+:   :+: :+:    :+:    :+:     :+:       :+:    :+:      :+:    :+: :+:    :+: :+:+:   :+: :+:    :+: :+:    :+: :+:        :+:   
    88888b                  :+:+:+  +:+ +:+    +:+    +:+     +:+       +:+             +:+        +:+    +:+ :+:+:+  +:+ +:+        +:+    +:+ +:+        +:+  
    888888b.                +#+ +:+ +#+ +#+    +:+    +#+     +#++:++#  +#++:++#++      +#+        +#+    +:+ +#+ +:+ +#+ +#++:++#++ +#+    +:+ +#+        +#++:++#    
    8888P"                  +#+  +#+#+# +#+    +#+    +#+     +#+              +#+      +#+        +#+    +#+ +#+  +#+#+#        +#+ +#+    +#+ +#+        +#+     
    P" `8.                  #+#   #+#+# #+#    #+#    #+#     #+#       #+#    #+#      #+#    #+# #+#    #+# #+#   #+#+# #+#    #+# #+#    #+# #+#        #+#    
        `8.   cgmm          ###    ####  ########     ###     ########## ########        ########   ########  ###    ####  ########   ########  ########## ########## 
        `8                  
"""


# Initial User Warning
clear_screen() # Initial Graphics clear_screen
print("NOTE: PLEASE RUN THIS WITH THE WORKING DIRECTORY AS BSCSF1")
pause()

# User Welcome
clear_screen() # Refresh Graphics
print(program_banner)
input("Welcome to Notes Console. Press Enter to continue...")

# User Menu
choice = False
while choice == False:
    
    clear_screen() # Refresh Graphics
    print(program_banner)
    
    number_of_menu_items = int(display_menu())
    
    choice = int(menu_choice())
    if choice >= 1 and choice <= number_of_menu_items:
        continue
    else:
        print(f"Option {choice} is not in range of menu")
        choice = False
        time.sleep(1)
        
# User Menu Result
clear_screen() # Refresh Graphics
print(program_banner)
print(f"Loading Option {choice}")
time.sleep(1)

## Menu Choice Resolver -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

menu_choice_resolver(choice)