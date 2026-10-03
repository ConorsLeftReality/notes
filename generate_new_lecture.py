## =====================================
## Generate New Lecture HTML File script
## =====================================
## Inputs:
## Lecture Title (str)
## Date (str) - DAY (int) MONTH (Long Form) YEAR (int*4)
## Module (str) - All caps, used to find directory and also used in title
## Lecturer (str)
## Link to slides (if None, avoid <a> tag, if link, put in <a href=""></a> tag)
##
## Processes:
## Takes inputs into variables
## Checks if module exists (if not, retry/ask if new)
## Lists current week directories in modules directory, asks which one to add to (and create option too)
## Creates base HTML with the variable inputs
##
## Output:
## Creates HTML file in the desired directory

## =======================================================================================
## ============================           FUNCTIONS          =============================
## =======================================================================================

def create_lecture_html_file(lecture_title,current_date,module_code,lecturer_name,slides_reference):
    
    # Try to generate the HTML File
    try:
        html_file = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{lecture_title}</title>
<link rel="stylesheet" href="../../win95.css">
<link rel="stylesheet" href="../../notes.css">
</head>

<body class="win95-desktop">

<div class="window notepad">

    <div class="title-bar">
    <div class="title-bar-text">{lecture_title} - Notepad</div>
    </div>

    <div class="notepad-body">

    <h1>{lecture_title}</h1>
    <p class="note-meta">{current_date} &middot; {module_code} &middot; {lecturer_name} &middot; Slides: {slides_reference}</p>


    <fieldset>
        <legend>Contents</legend>
        <ul class="list-arrow">
        <li><a href="#sec-intro">INTRODUCTION SECTION</a></li>
        
        <!--
        <li><a href="#sec-id">SECTION_NAME</a></li>
        -->
        
        </ul>
    </fieldset>


    <section class="note-section" id="sec-intro">
    
        <h2>INTRODUCTION_SECTION</h2>
        <p>ENTER_TEXT_HERE</p>
        
    </section>
    
    <!-- SECTION TEMPLATE -->
    <!--
    
    <section class="note-section" id="sec-id">
            
            <h2>INTRODUCTION_SECTION</h2>
            <p>ENTER_TEXT_HERE</p>
            
    </section>
    
    -->
    
    </div>

    <div class="status-bar">
    <p class="status-bar-field">{lecture_title}</p>
    <p class="status-bar-field">{current_date}</p>
    </div>
</div>

<!-- Taskbar -->
<div class="taskbar">
    <a class="start-button" href="../../index.html">Start</a>
    <div class="taskbar-divider"></div>

    <ul class="taskbar-nav">
    <li><a class="taskbar-item" href="../{module_code.lower()}_index.html">Back to {module_code} Home</a></li>
    </ul>
</div>

</body>
</html>
        """
        # Return Success (True) and the HTML file for saving to directory
        return True, html_file
    
    # IF ERROR
    except Exception as error_msg:
        # Return Fail (False) and the error
        return False, error_msg
    
def make_directory(directory_name):
    
    try:
        os.mkdir(directory_name)
        print(f"Directory '{directory_name}' Created")
        return True # Success
    
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory_name}'. Try to run this file as administrator?")
        return False # Fail
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return False # Fail
    
def write_module_index_page_html(module_code,acknowledged_known_module_directories):
    try:
        
        ## (1) Create Module Lecture contents element ===================================================================
        WEEKS_IN_MODULE_DIR = os.listdir(f"{module_code}/")
        module_lecture_contents = ""
        if WEEKS_IN_MODULE_DIR == []:
            module_lecture_contents = """
            <h3>No Lectures yet</h3>
            """ 
        else:
            for week in WEEKS_IN_MODULE_DIR:
                if "." in week:
                    continue
                else:
                    week_corrected = (week.capitalize()).replace("_"," ")
                    module_lecture_contents = module_lecture_contents + f"\n\t\t\t\t\t<h3>{week_corrected}</h3>\n" + "\t\t\t\t\t\t<ul class=\"list-arrow\">\n"
                    
                    FILES_IN_WEEK = os.listdir(f"{module_code}/{week}/")
                    
                    for file in FILES_IN_WEEK:
                        #file_without_extension = file[0:file.index(".")]
                        #print(file_without_extension)
                        module_lecture_contents = module_lecture_contents + f"\t\t\t\t\t\t\t<li><a href=\"{week}/{file}\">{file}</a></li>\n"
                        
                    module_lecture_contents = module_lecture_contents + "\t\t\t\t\t\t</ul>\n"
                    
                
        ## (2) Create Taskbar list element ==============================================================================
        taskbar_of_modules = ""
        acknowledged_known_module_directories.append(module_code)
        acknowledged_known_module_directories.sort() # Sort it for the Taskbar to be in correct order

        taskbar_of_modules = taskbar_of_modules + f"\t<li><a class=\"taskbar-item\" href=\"../index.html\">Home</a></li> \n"
        for module_directory in acknowledged_known_module_directories:
            if module_directory == module_code:
                print("Made own module")
                taskbar_of_modules = taskbar_of_modules + f"\t\t\t\t\t<li><a class=\"taskbar-item active\" href=\"../{module_directory}/{(module_directory.lower())}_index.html\">{module_directory}</a></li> \n"
                acknowledged_known_module_directories.remove(module_directory)
            elif module_directory != module_code:
                print("Made other module")
                taskbar_of_modules = taskbar_of_modules + f"\t\t\t\t\t<li><a class=\"taskbar-item\" href=\"../{module_directory}/{(module_directory.lower())}_index.html\">{module_directory}</a></li> \n"
        
        ## (4) Create message for specific module
        
        module_message = "NEW MODULE, ADD MESSAGE IN FILE - Conor"
        
        # Module Messages are stored in seperate file
        # FORMAT: MODULECODE, "message here"
        with open("module_messages.txt") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue # Skip blank lines

                # Split on first comma only
                module, message = line.split(",", 1)
                
                if module == module_code:
                    module_message = message
                    
    
        ## (3) Create full HTML file ====================================================================================
        
        html_file = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{module_code} - Lecture Index</title>
  
  <link rel="stylesheet" href="../win95.css">
  <link rel="stylesheet" href="../notes.css">
</head>

<body class="win95-desktop">

  <div class="window notepad">
    <div class="title-bar">
      <div class="title-bar-text">{module_code} - Lecture Index</div>
    </div>

    <div class="notepad-body">
      <h1>{module_code} - Lecture Index</h1>
      <p class="note-meta">Semester 1 &middot; Lecture Index</p>

      <section class="note-section">
        <h2>Lectures</h2>
        
         {module_lecture_contents}
      </section>
    
      <aside class="callout">
        <span class="callout-title">Message of the day!</span>
        <p>{module_message}</p>
      </aside>

    </div>

    <div class="status-bar">
      <p class="status-bar-field">Status: working</p>
    </div>
  </div>


  <!-- ======================================================================
       TASKBAR MENU
       On each page, put class="active" on that page's own link 
       and remove it from the others.
       ====================================================================== 
  -->
  
  <div class="taskbar">
    <a class="start-button" href="../index.html">Start</a>
    <div class="taskbar-divider"></div>

    <ul class="taskbar-nav">

        {taskbar_of_modules}

    </ul>
  </div>

</body>
</html>
"""
        #print(html_file)
        return True, html_file
    
    except Exception as e: # Fail in generation
        return False, e
    
def pause():
    input("<<< Press ENTER to continue >>>")
    
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

## =======================================================================================
## ============================     MAIN CODE FOR SCRIPT    ==============================
## =======================================================================================
import os
import time

# Clear Terminal before use
clear_screen()

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
        print("<<< SYSTEM >>>No value for date, enter a value to continue")
        date = str(input("Date of Lecture (E.G. \"12 October 2026\", no symbols) >>> "))
        
        if date != "":
            date_null_resolved = True
      
# Fix Module NULL
if lecture_module == "":
    module_null_resolved = False
    while module_null_resolved == False:
        clear_screen()
        print("<<< SYSTEM >>>No value for Module, enter a value to continue")
        lecture_module = (str(input("Lecture's Module >>> "))).upper()
        
        if lecture_module != "":
            module_null_resolved = True
            
# Fix Lecturer name NULL
if name_of_lecturer == "":
    name_of_lecturer = "UNDEFINED_LECTURER_NAME"
            
# Fix slides NULL
if slides_link == "":
    slides_link = "UNSPECIFIED"

## (2) Search for Module Directory ===========================================================================================================
# Create a loop for this section until we get a result we can use
module_selection_resolved = False
while module_selection_resolved == False:
    
    clear_screen()
    
    files_in_working_dir = os.listdir() # Make list of files in working dir.
    ENROLLED_MODULES = ["CS1106","CS1110","CS1111","CS1112","CS1113","CS1115","CS1116","CS1117","MA1001","MA1002"] # Specify the modules that I actually study
    
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
        print(f"<<< SYSTEM >>> MODULE FOLDER DOESNT EXIST FOR {lecture_module} YET, BUT YOU ARE ENROLLED IN THIS MODULE")
        print("<<< SYSTEM >>> CREATING MODULE FOLDER NOW...")
        
        # Try make directory, if success, continue
        if make_directory(lecture_module): # Error messages handled by function
            module_selection_resolved = True
            
        
    elif lecture_module in files_in_working_dir:
        print(f"<<< SYSTEM >>> FOUND MODULE FOLDER FOR {lecture_module}, UNSURE IF ENROLLED (Please update!!)")
        pause()
        module_selection_resolved = True
        
    # Uh oh, no folder found and not a module we take, either custom note, typo or has modules wrong
    else:
        print(f"<<< SYSTEM >>> NO MODULE FOLDER FOUND FOR {lecture_module}")
        print("OPTIONS")
        print("================================================")
        print("CONTINUE AND CREATE FOLDER?                  (Y)")
        print("ENTER NEW MODULE CODE?                       (N)")
        print("VIEW FOLDERS ACCESSIBLE AND ENROLLED MODULES (F)")
        user_choice = (input(" >>> ")).upper()
        
        if user_choice == "Y":
            # Try make directory, if success, continue
            if make_directory(lecture_module): # Error messages handled by function
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

## (3) Determine the week the lecture notes belong in ========================================================================================

week_selection_resolved = False
while week_selection_resolved == False:
    
    clear_screen()
    
    files_in_module_dir = os.listdir(lecture_module) # Make list of files in modules dir.
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
        proceed_confirmation = (input(f"This week isnt in the folder, continue to make folder for week '{week_selected}'? (Y/N) >>>")).upper()
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
            
        
## (4) Generate the HTML File from the data collected earlier

success,data = create_lecture_html_file(title_of_lecture,date,lecture_module,name_of_lecturer,slides_link)

if success:
    print("<<< SYSTEM >>> SUCCESS IN HTML FILE GENERATION")
else:
    print(f"ERROR IN HTML FILE GENERATION: {data}")
    
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


## (6) Remake the Index page, whether new or existing folder

success,data = write_module_index_page_html(lecture_module,current_module_folders)
if success:
    print("<<< SYSTEM >>> SUCCESS IN INDEX FILE GENERATION/UPDATING")
    module_selection_resolved = True
    
    ## (6a) Write Index page to folder
    filename = f"{(lecture_module).lower()}_index.html"
    filepath = f"{lecture_module}/{filename}"
    with open(filepath, "w") as f:
        f.write(data)
        f.close()
    print("<<< SYSTEM >>> SUCCESS IN INDEX FILE OVERWRITE")
    
else:
    print(f"ERROR IN INDEX FILE GENERATION/UPDATING: {data}")
    module_selection_resolved = False

print("<<< SCRIPT FINISHED >>>")

## TODO: Make a modules file, and write modules to it when confirmed that we want to make it, because currently they dont show on taskbar