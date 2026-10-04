## -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def lecture_notes_generation_script(
    lecture_information_collection,
    module_selection_resolver,
    week_selection_resolver,
    create_lecture_html_file,
    write_lecture_notes_html,
    create_module_index_page_html,
    write_index_file_to_module
    ):
    
    ## (1) Collect information on lecture
    title_of_lecture,date,lecture_module,name_of_lecturer,slides_link = lecture_information_collection


    ## (2) Find Module Directory ===========================================================================================================
    current_module_folders = module_selection_resolver()

    ## (3) Find Week User wants to write to ================================================================================================
    week_selected = week_selection_resolver(lecture_module)
                
    ## (4) Generate the HTML File from the data collected earlier
    success,data = create_lecture_html_file(title_of_lecture,date,lecture_module,name_of_lecturer,slides_link)

    if success:
        print("<<< SYSTEM >>> SUCCESS IN HTML FILE GENERATION")
    else:
        print(f"ERROR IN HTML FILE GENERATION: {data}")

    ## (5) Write the data to the location determined in Pt. 2 and Pt. 3
    write_lecture_notes_html(date,lecture_module,week_selected,data)


    ## (6) Remake the Index page, whether new or existing folder
    success,data = create_module_index_page_html(lecture_module,current_module_folders)

    if success:
        print("<<< SYSTEM >>> SUCCESS IN NEW INDEX FILE GENERATION")
        write_index_file_to_module()
    else:
        print(f"ERROR IN INDEX FILE GENERATION/UPDATING: {data}")

    print("<<< LECTURE NOTE WRITE SCRIPT FINISHED >>>")
    
## -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## END OF FILE