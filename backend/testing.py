import os

repository_root_directory = "C:/Users/conormasterson/Documents/BSCSF1" # Set this as absolute path to repo, replace back slashes with forward slashes
os.chdir(repository_root_directory)

from modules.database_manipulation import check_enrolled_modules, update_enrollment_of_module

# print("Here are the enrolled modules")
# ENROLLED_MODULES = check_enrolled_modules()
# print(ENROLLED_MODULES)

# print("Unenrolling CS1106")
# update_enrollment_of_module("CS1106",0)

# print("Here are the enrolled modules")
# ENROLLED_MODULES = check_enrolled_modules()
# print(ENROLLED_MODULES)

# print("Enrolling CS1106")
# update_enrollment_of_module("CS1106",1)

# print("Here are the enrolled modules")
# ENROLLED_MODULES = check_enrolled_modules()
# print(ENROLLED_MODULES)