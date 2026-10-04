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

## GENERATION MODULE    - Clear Screen, make directory (MKDIR), Generate Module Index Page (MODULE_INDEX_PAGE), 
##                        Generate Lecture File (LECTURE_FILE), Generate Main Index Page (MAIN_INDEX_PAGE)
##                      - USED TO GENERATE FILES OR DIRECTORIES
from modules.generate import make_directory,create_module_index_page_html,create_lecture_html_file


## DATA MANIPULATION MODULE - Collects user inputs about a lecture, resolves and creates a modules directory, Enrolled Module file updating, 
##                            Module Messages file updating
##                          - USED TO COLLECT, WORK WITH, AND MANIPULATE DATA
from modules.data_manipulator import lecture_information_collection,module_selection_resolver,week_selection_resolver,write_lecture_notes_html,write_index_file_to_module #enrolled_modules_update, module_messages_update


## UTILITIES MODULE     - pause, clear screen
##                      - VARIOUS USES, READ module_documentation.txt in /backend
from modules.utilities import pause,clear_screen

## ====================================================================
## ========================== IMPORT SCRIPTS ==========================
## ====================================================================

## LECTURE NOTES GENERATION SCRIPT  - lecture notes generation script
##                                  - Used to call the main script for lecture notes generation
from modules.lecture_note_generate import lecture_notes_generation_script


## =======================================================================================
## ============================     MAIN CODE FOR PROGRAM    ==============================
## =======================================================================================

# Clear Terminal before use
clear_screen()
print("NOTE: PLEASE RUN THIS WITH THE WORKING DIRECTORY AS BSCSF1")


lecture_notes_generation_script(
    lecture_information_collection,
    module_selection_resolver,
    week_selection_resolver,
    create_lecture_html_file,
    write_lecture_notes_html,
    create_module_index_page_html,
    write_index_file_to_module
    )

## TODO: Make the program regenerate/update all index files if asked to, as new modules wont be indexed if generated
## TODO: Make program update the main index page with new module folders, and have title for module too (in file)