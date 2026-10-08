## ====================================================================
## ========================== IMPORT MODULES ==========================
## ====================================================================

import time
import os
import sqlite3

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

def check_enrolled_modules():
    try:
        # Connect to SQLite Database and create a cursor
        sqliteConnection = sqlite3.connect('backend/data/notes.db')
        
        # Specifies only look at row 0 (Returns a properly formatted list) 
        # (https://stackoverflow.com/questions/2854011/get-a-list-of-field-values-from-pythons-sqlite3-not-tuples-representing-rows)
        sqliteConnection.row_factory = lambda cursor, row: row[0] 
        
        cursor = sqliteConnection.cursor()
        #print('DB Init')

        # Execute query to find which modules are enrolled
        query = 'SELECT module_id FROM modules WHERE enrolled = 1;'
        cursor.execute(query)
        
        # Fetch and print the result
        result = cursor.fetchall()
        #print(result)

        # Close the cursor after use
        cursor.close()

    except sqlite3.Error as error:
        print(f"ERROR IN DATABASE CONNECTION / DATABASE INTERACTION: {error}")
        return None

    finally:
        # Ensure the database connection is closed
        if sqliteConnection:
            sqliteConnection.close()
        
    return result

## -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def update_enrollment_of_module(module_code,enrollment):
#                                 String   , Integer
    
    try:
        # Connect to SQLite Database and create a cursor
        sqliteConnection = sqlite3.connect('backend/data/notes.db')
        
        cursor = sqliteConnection.cursor()
        #print('DB Init')
        
        query = 'UPDATE modules SET enrolled = ? WHERE module_id = ?;'
        cursor.execute(query, (enrollment, module_code))

        sqliteConnection.commit()

        if cursor.rowcount == 0:
            print(f"No module found with id {module_code}")

        cursor.close()

    except sqlite3.Error as error:
        print(f"ERROR IN DATABASE CONNECTION / DATABASE INTERACTION: {error}")
        return

    finally:
        # Ensure the database connection is closed
        if sqliteConnection:
            sqliteConnection.close()
        
    return

## -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def fetch_module_message(module_code):
    try:
        # Connect to SQLite Database and create a cursor
        sqliteConnection = sqlite3.connect('backend/data/notes.db')
        
        # Specifies only look at row 0 (Returns a properly formatted list) 
        # (https://stackoverflow.com/questions/2854011/get-a-list-of-field-values-from-pythons-sqlite3-not-tuples-representing-rows)
        sqliteConnection.row_factory = lambda cursor, row: row[0] 
                
        cursor = sqliteConnection.cursor()
        #print('DB Init')

        # Execute query to find which modules are enrolled
        query = f'SELECT module_message FROM modules WHERE module_id = \'{module_code}\';'
        cursor.execute(query)
        
        # Fetch and print the result
        if cursor.fetchall() != []:
            module_message = (cursor.fetchall())[0] # As we only get one message, the first in the returned list will be the module message
        else:
            module_message = "No message for this module, try again another time!"
        #print(result)

        # Close the cursor after use
        cursor.close()

    except sqlite3.Error as error:
        print(f"ERROR IN DATABASE CONNECTION / DATABASE INTERACTION: {error}")
        return None

    finally:
        # Ensure the database connection is closed
        if sqliteConnection:
            sqliteConnection.close()
        
    return module_message
    
## -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def filename_not_in_lecture_table_db(filename):
    try:
        # Connect to SQLite Database and create a cursor
        sqliteConnection = sqlite3.connect('backend/data/notes.db')
        
        # Specifies only look at row 0 (Returns a properly formatted list) 
        # (https://stackoverflow.com/questions/2854011/get-a-list-of-field-values-from-pythons-sqlite3-not-tuples-representing-rows)
        sqliteConnection.row_factory = lambda cursor, row: row[0] 
        
        cursor = sqliteConnection.cursor()
        #print('DB Init')

        # Execute query to find which modules are enrolled
        query = f'SELECT filename FROM lectures WHERE filename = \'{filename}\';'
        cursor.execute(query)
        
        # Fetch and print the result
        result = cursor.fetchall()

        # Close the cursor after use
        cursor.close()

    except sqlite3.Error as error:
        print(f"ERROR IN DATABASE CONNECTION / DATABASE INTERACTION: {error}")
        return None

    finally:
        # Ensure the database connection is closed
        if sqliteConnection:
            sqliteConnection.close()
    
    # Check if file exists
    if filename in result:
        return True
    else:
        return False 
    
## -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def add_to_lectures_db(module_code,week,filename):
    try:
        # Connect to SQLite Database and create a cursor
        sqliteConnection = sqlite3.connect('backend/data/notes.db')
        
        # Specifies only look at row 0 (Returns a properly formatted list) 
        # (https://stackoverflow.com/questions/2854011/get-a-list-of-field-values-from-pythons-sqlite3-not-tuples-representing-rows)
        sqliteConnection.row_factory = lambda cursor, row: row[0] 
        
        cursor = sqliteConnection.cursor()
        
        ## Define week
        week_input = week[week.index("_")+1:]
        
        print(filename)
        
        ## Define created_at
        underscore = filename.index("_")
        dot = filename.index(".")
    
        #print(underscore)
        
        day = filename[0:underscore]
        if len(day) == 1:
            day = f"0{day}"
        #print(day)
        month = filename[underscore+1:dot-5]
        #print(month)
        year = filename[dot-4:dot]
        #print(year)
        
        MONTHS = ["january", "february", "march", "april", "may", "june",
          "july", "august", "september", "october", "november", "december"]

        month_numerical = MONTHS.index(month) + 1
        
        created_at_input = f"{year}-{month_numerical}-{day} 00:00:00"
        
        #print(created_at_input)
        
        # Execute query to write record
        query = f"""
        INSERT INTO lectures 
        VALUES                  (NULL, 'UNSPECIFIED', '{module_code}', '{created_at_input}', NULL, '{week_input}', '{filename}');
        """
        
        print(query)
        
        cursor.execute(query)
        
        # Fetch and print the result
        sqliteConnection.commit()

        # Close the cursor after use
        cursor.close()

    except sqlite3.Error as error:
        print(f"ERROR IN DATABASE CONNECTION / DATABASE INTERACTION: {error}")
        return None

    finally:
        # Ensure the database connection is closed
        if sqliteConnection:
            sqliteConnection.close()
    
    return None