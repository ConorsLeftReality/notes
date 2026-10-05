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

## ====================================================================
## ========================== IMPORT MODULES ==========================
## ====================================================================

import os

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

## -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def make_directory(directory_name):
    
    try:
        os.mkdir(f"{directory_name}")
        print(f"Directory '{directory_name}' Created")
        return True # Success
    
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory_name}'. Try to run this file as administrator?")
        return False # Fail
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return False # Fail

## -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def create_module_index_page_html(module_code,acknowledged_known_module_directories):
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
                #print("Made own module")
                taskbar_of_modules = taskbar_of_modules + f"\t\t\t\t\t<li><a class=\"taskbar-item active\" href=\"../{module_directory}/{(module_directory.lower())}_index.html\">{module_directory}</a></li> \n"
                acknowledged_known_module_directories.remove(module_directory)
                continue
            elif module_directory != module_code:
                #print("Made other module")
                taskbar_of_modules = taskbar_of_modules + f"\t\t\t\t\t<li><a class=\"taskbar-item\" href=\"../{module_directory}/{(module_directory.lower())}_index.html\">{module_directory}</a></li> \n"
                continue
        
        ## (4) Create message for specific module
        
        module_message = "NEW MODULE, ADD MESSAGE IN FILE - Conor"
        
        # Module Messages are stored in seperate file
        # FORMAT: MODULECODE, "message here"
        with open("backend/data/module_messages.txt") as f:
            for line in f:
                line = line.strip()
                if not line or (line.strip(" "))[0] == "#":
                    continue # Skip blank lines

                # Split on first comma only
                module, message = line.split(",", 1)
                
                if module == module_code:
                    module_message = message
                    
    
        ## (5) Create full HTML file ====================================================================================
        
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

## -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## END OF FILE