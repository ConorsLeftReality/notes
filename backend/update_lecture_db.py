## Input
##
## DocumentRoot for Repository

## Processes
##
## 1.   find which modules we are enrolled in (take as given that all modules are logged)
##      make list of directories to iterate through (this exists already)
## 2.   make list of weeks (this function exists somewhere already too)
## 3.   make list of lecture filenames
##      log filename
## 4.   if filename isnt a value for a filename in the database, 
#
#       WRITE TO DB WITH: 
#       id as NULL (Autoincrement will fill this in),
#       title as "UNSPECIFIED", 
#       Module Code as the code of the module directory we are in currently, 
#       created_at as the filename (with "_" replaced with " " and properly capitalised) and time 00:00:00,
#       Slides link as NULL, 
#       week as the value after the underscore in week_xx,
#       and filename as the filename
#
# rinse, repeat

import os
import sys
from modules.database_manipulation import check_enrolled_modules, filename_not_in_lecture_table_db, add_to_lectures_db

# INITIALLY, lets move to the working directory for repo

repository_root_directory = "C:/Users/conormasterson/Documents/BSCSF1" # Set this as absolute path to repo, replace back slashes with forward slashes

try: 
    os.chdir(repository_root_directory)
except Exception as e:
    print(f"Error setting working directory: {e}")
    input("Press Enter to exit...")
    sys.exit(0)

## OK LETS START

## 1. Make a list of Module directories

files_in_working_dir = os.listdir() # Make list of files in working dir.

ENROLLED_MODULES = check_enrolled_modules() # Check what modules currently enrolled in

PRESENT_ENROLLED_MODULES = []
for file in files_in_working_dir: 
    if file in ENROLLED_MODULES:
        PRESENT_ENROLLED_MODULES.append(file)
        
for module_directory in PRESENT_ENROLLED_MODULES:
    
    ## 2. Make a list of week directories in a given module
    
    files_in_module_dir = os.listdir(f"{module_directory}") # Make list of files in modules dir.
    WEEKS_IN_DIRECTORY = []
    
    for content in files_in_module_dir:
        if "index" not in content and "files" not in content and ".html" not in content:
            WEEKS_IN_DIRECTORY.append(content)
    #print(WEEKS_IN_DIRECTORY)
            
    ## 3. Make list of lecture files in directory
    for week in WEEKS_IN_DIRECTORY:
        files_in_module_dir = os.listdir(f"{module_directory}/{week}") # Make list of files in week's dir.
        LECTURES_IN_DIRECTORY = []
        
        for content in files_in_module_dir:
            LECTURES_IN_DIRECTORY.append(content)
        
        for lecture in LECTURES_IN_DIRECTORY:
            if filename_not_in_lecture_table_db(lecture):
                print("File Exists!")
            else:
                print("File does not exist, creating record")
                add_to_lectures_db(module_directory,week,lecture)
                
                