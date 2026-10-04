## ====================================================================
## ========================== IMPORT MODULES ==========================
## ====================================================================

import time
import os

## UTILITIES MODULE     - pause, clear screen
##                      - VARIOUS USES, READ module_documentation.txt in /backend
from modules.utilities import pause,clear_screen

## UTILITIES MODULE     - display menu,
##                      - User Interface, usually graphical functions
from modules.main_program_ui import display_menu, menu_choice

## GENERATION MODULE    - Clear Screen, make directory (MKDIR), Generate Module Index Page (MODULE_INDEX_PAGE), 
##                        Generate Lecture File (LECTURE_FILE), Generate Main Index Page (MAIN_INDEX_PAGE)
##                      - USED TO GENERATE FILES OR DIRECTORIES
from modules.generate import make_directory,create_module_index_page_html,create_lecture_html_file

## ====================================================================
## ========================== IMPORT SCRIPTS ==========================
## ====================================================================

## LECTURE NOTES GENERATION SCRIPT  - lecture notes generation script
##                                  - Used to call the main script for lecture notes generation
from modules.lecture_note_generate import lecture_notes_generation_script

## -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def lecture_information_collection():
    title_of_lecture =  str(input("Lecture Title                                        >>> "))
    date =            str(input("Date of Lecture (E.G. \"12 October 2026\", no symbols) >>> "))
    lecture_module =   (str(input("Lecture's Module                                     >>> "))).upper()
    name_of_lecturer =  str(input("Name of Lecturer                                     >>> "))
    slides_link =       str(input("Link to slides?                                      >>> "))

    ## (1) Fix null spaces ===========================================================================================================

    # Fix title NULL
    if title_of_lecture == "":
        title_of_lecture == "UNSPECIFIED_TITLE_AUTOGENERATE"

    # Fix date NULL
    if date == "":
        date_null_resolved = False
        while date_null_resolved == False:
            clear_screen()
            print("<<< SYSTEM >>> No value for date, enter a value to continue")
            date = str(input("Date of Lecture (E.G. \"12 October 2026\", no symbols) >>> "))
            
            if date != "":
                date_null_resolved = True
        
    # Fix Module NULL
    if lecture_module == "":
        module_null_resolved = False
        while module_null_resolved == False:
            clear_screen()
            print("<<< SYSTEM >>> No value for Module, enter a value to continue")
            lecture_module = (str(input("Lecture's Module >>> "))).upper()
            
            if lecture_module != "":
                module_null_resolved = True
                
    # Fix Lecturer name NULL
    if name_of_lecturer == "":
        name_of_lecturer = "UNDEFINED_LECTURER_NAME"
                
    # Fix slides NULL
    if slides_link == "":
        slides_link = "UNSPECIFIED"
        
    return title_of_lecture,date,lecture_module,name_of_lecturer,slides_link

## -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def module_selection_resolver(lecture_module):
    
    module_selection_resolved = False
    while module_selection_resolved == False:
        
        clear_screen()
        
        files_in_working_dir = os.listdir() # Make list of files in working dir.
        ENROLLED_MODULES = [] # Establish list to specify the modules that I actually study
        
        with open("backend/data/enrolled_modules.txt","r") as f:
            for module in f:
                if module.strip("\n") == "" or (module.strip(" "))[0] == "#":
                    continue
                else:
                    module = module.strip("\n")
                    ENROLLED_MODULES.append(str(module))
        
        # Search through folders we can see from our working directory, if any match our enrolled modules, then add to a list so we know this
        current_module_folders = []
        
        for file in files_in_working_dir:
            if file in ENROLLED_MODULES:
                current_module_folders.append(file) # Add to list so we know this directory exists


        # MODULE SELECTION RESOLUTION
        
        # Now check if the lecture module has a folder. If does, continue. If not, ask what to do.
        # ISOK, continue
        if lecture_module in current_module_folders:
            print(f"<<< SYSTEM >>> FOUND ENROLLED MODULE FOLDER FOR {lecture_module}")
            module_selection_resolved = True
            pause()
            
        # ISOK kinda, folder doesnt exist yet, and its a module we take so make folder then continue
        elif lecture_module not in current_module_folders and lecture_module in ENROLLED_MODULES:
            print(f"<<< SYSTEM >>> MODULE FOLDER DOESNT EXIST FOR {lecture_module}, BUT YOU ARE ENROLLED IN THIS MODULE")
            print("<<< SYSTEM >>> CREATING MODULE FOLDER NOW...")
            pause()
            
            # Try make directory, if success, continue
            status = make_directory(lecture_module)
            pause()
            if status: # Error messages handled by function
                module_selection_resolved = True
                
            
        elif lecture_module in files_in_working_dir:
            print(f"<<< SYSTEM >>> FOUND MODULE FOLDER FOR {lecture_module}, UNSURE IF ENROLLED (Please update enrolled_modules.txt!!)")
            pause()
            module_selection_resolved = True
            
        # Uh oh, no folder found and not a module we take, either custom note, typo or has modules wrong
        else:
            print(f"<<< SYSTEM >>> NO MODULE FOLDER FOUND FOR {lecture_module}")
            print("OPTIONS")
            print("================================================")
            print("CONTINUE, ENROLL AND CREATE FOLDER?          (Y)")
            print("ENTER NEW MODULE CODE?                       (N)")
            print("VIEW FOLDERS ACCESSIBLE AND ENROLLED MODULES (F)")
            user_choice = (input(" >>> ")).upper()
            
            if user_choice == "Y":
                # Try make directory, if success, continue
                if make_directory(lecture_module): # Error messages handled by function
                    with open("backend/data/enrolled_modules.txt", "a") as f:
                        f.write(f"\n{lecture_module}")
                        f.close()
                    module_selection_resolved = True
            
            elif user_choice == "N":
                lecture_module = (input("Lecture's Module >>> ")).upper()
                
            elif user_choice == "F":
                print("<<< SYSTEM >>> These are the folders in your current working directory (the folder this program is running within)")
                print(files_in_working_dir)
                print("<<< SYSTEM >>> These are the modules you are enrolled in")
                print(ENROLLED_MODULES)
                pause()
                
            else:
                print("INVALID CHOICE")
                time.sleep(2)
            
    return current_module_folders

## -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def week_selection_resolver(lecture_module):
    ## Determine the week the lecture notes belong in
    week_selection_resolved = False
    while week_selection_resolved == False:
        
        clear_screen()
        
        files_in_module_dir = os.listdir(f"{lecture_module}") # Make list of files in modules dir.
        weeks_in_directory = []
        
        for content in files_in_module_dir:
            if "index" not in content:
                weeks_in_directory.append(content)
        
        print(" <<< SYSTEM >>> Here are the weeks in the folder:")  
        for week in weeks_in_directory:
            if week != weeks_in_directory[-1]:
                print(week,end=", ")
            else:
                print(week)
        
        print("")
        
        week_selected = str(input("Which week would you like to write this file to? (E.G. week_#, or type a new week if desired)\n >>> "))
        
        # WEEK SECTION RESOLUTION
        if week_selected in weeks_in_directory:
            week_selection_resolved = True
            
        elif week_selected not in weeks_in_directory and week_selected != "":
            clear_screen()
            proceed_confirmation = (input(f"This week isnt in the folder, continue to make folder for week '{week_selected}'? (Y/N) >>> ")).upper()
            if proceed_confirmation == "Y":
                if make_directory(f"{lecture_module}/{week_selected}"):
                    week_selection_resolved = True
                else:
                    clear_screen()
                    print("<<< SYSTEM >>> Error in Directory Creation")
                    week_selection_resolved = False
                    pause()
        
        elif "_" not in week_selected:
            clear_screen()
            print("<<< SYSTEM >>> You must have an underscore in the weeks name, between \"Week\" and the week number.")
            week_selection_resolved = False
            pause()
                    
        elif week_selected == "":
            clear_screen()
            print("<<< SYSTEM >>> Please enter a week to continue!")
            week_selection_resolved = False
            pause()     
        
    return week_selected  
       
## -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
     
def write_lecture_notes_html(date,lecture_module,week_selected,data):
    ## (5) Write the data to the location determined in Pt. 2 and Pt. 3

    ## (5a) Resolve filename
    filename = f"{(date.replace(" ","_")).lower()}.html" # Create Filename for lecture note
    i = 1 # Incase file already exists, create variable out of loop

    filename_resolved = False
    while filename_resolved == False:

        if filename in os.listdir(f"{lecture_module}/{week_selected}/"):
            filename = f"{(date.replace(" ","_")).lower()}_{i}.html"
            i += 1
            continue
        else:
            filename_resolved = True # Explicity means we exit loop

    filepath = f"{lecture_module}/{week_selected}/{filename}"

    ## (5b) Write data to file under filename
    with open(filepath, "w") as f:
        f.write(data)
        f.close()

## -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  
def write_index_file_to_module(lecture_module,data):
    ## (6a) Write Index page to folder
        filename = f"{(lecture_module).lower()}_index.html"
        filepath = f"{lecture_module}/{filename}"
        with open(filepath, "w") as f:
            f.write(data)
            f.close()
        print("<<< SYSTEM >>> SUCCESS IN INDEX FILE OVERWRITE")
    
## -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def menu_choice_resolver(number):
    if number == 1:
        lecture_notes_generation_script(
        lecture_information_collection,
        module_selection_resolver,
        week_selection_resolver,
        create_lecture_html_file,
        write_lecture_notes_html,
        create_module_index_page_html,
        write_index_file_to_module
        )
## END OF FILE