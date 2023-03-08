#!/usr/bin/env python

"""my_shell_outline.py:
Simple shell that interacts with the filesystem, e.g., try "PShell>files".

Try to stick to Style Guide for Python Code and Docstring Conventions:
see https://peps.python.org/pep-0008 and https://peps.python.org/pep-0257/

(Note: The breakdown into Input/Action/Output in this script is just a suggestion.)
"""

import glob
import os
import pwd
import shutil
import sys
import time



# ========================
#    files command
#    List file and directory names
#    No command arguments
# ========================
def files_cmd(fields):
	if checkArgs(fields, 0):
		for filename in os.listdir('.'):
			print("File Name:", filename)
			type = "file"
			if os.path.isdir(filename): type = "directory"
			print("File/Directory:", type)
	else: print("File does not exist")


# ========================
#  info command
#     List file information
#     1 command argument: file name
# ========================
def info_cmd(fields):
	if checkArgs(fields, 1):
		filename = fields[1]
		if checkExists(filename):
			print("File Name:", filename)
			type = "file"
			if os.path.isdir(filename): type = "directory"
			print("File/Directory:", type)
			print("Owner:", pwd.getpwuid(os.stat(filename).st_uid).pw_name)
			print("Last Modified:", time.ctime(os.path.getmtime(filename)))
			print("Size:", os.path.getsize(filename))
			try:
				f = open(filename)
				print("Executable?: True")
			except:
				print("Executable?: False")
		else: print("File does not exist")
		

def delete_cmd(fields):
	if checkArgs(fields, 1):
		filename = fields[1]
		if checkExists(filename):	#checks args and if file exists
			if os.path.isdir(filename): print("Cannot delete directories"); return 0
			try:
				os.remove(filename)	
				print("File Deleted")
			except:
				print("Permission error")	#if an error occurs, output line to user
		else: print("File does not exist")
		


def copy_cmd(fields):
	if checkArgs(fields, 2):
		fromfile = fields[1]
		tofile = fields[2]
		if checkExists(fromfile) and not checkExists(tofile):	#checks if from file exists and to file doesn't
			try:
				shutil.copy2(fromfile, tofile)	#copies file
				print("File copied")
			except:
				print("Permission error")	#gives error messages
		else: print("1st file must exist and 2nd files must not")
		

			
def where_cmd(fields):
	if checkArgs(fields, 0):
		print(os.getcwd())	#output dir line
		

		
def down_cmd(fields):
	if checkArgs(fields, 1):
		path = fields[1]
		if checkExists(path):	#checks if dir exists
			os.chdir(path)	#then moves to the dir
			print("Directory moved down")
		else: print("Path does not exist")



def up_cmd(fields):
	if checkArgs(fields, 0):
		curr = os.getcwd()
		os.chdir("..")	#uses .. to up a directory
		new = os.getcwd()
		if curr == new: print("Root directory")	#if the old directory was the same as the new one, output root dir line
		else: print("Directory moved up")
		
        
		
def exit_cmd(fields):
	if checkArgs(fields, 0):
		sys.exit()	#checks args and exits

# ----------------------
# Other functions
# ----------------------
def checkArgs(fields, num):
    """Returns if len(fields)-1 == num and print an error in shell if not.
    
    Input: takes a list of text fields and how many non-command fields are expected
    Action: prints error to shell if the number of fields is unexpected
    Output: returns boolean value to indicate if it was expected number of fields
    """

    numArgs = len(fields) - 1
    if numArgs == num:
        return True
    if numArgs > num:
        print("Unexpected argument", fields[num+1], "for command", fields[0])
    else:
        print("Missing argument for command", fields[0])
        
    return False


def checkExists(filename):	#method that returns true if file exists and false otherwise
	if os.path.exists(filename):
		return True
	else: 
		return False
# ---------------------------------------------------------------------

def main():
    """Returns exit code 0 (after executing the main part of this script).
    
    Input: no function arguments
    Action: run multiple user-inputted commands
    Output: return zero to indicate regular termination
    """
    
    while True:
        line = input("PShell>")
        fields = line.split()
        # split the command into fields stored in the fields list
        # fields[0] is the command name and anything that follows (if it follows) is an argument to the command
        print()
	
        if fields[0] == "files":
            files_cmd(fields)
        elif fields[0] == "info":
        	info_cmd(fields)
        elif fields[0] == "delete":
        	delete_cmd(fields)
        elif fields[0] == "copy":
        	copy_cmd(fields)
        elif fields[0] == "where":
        	where_cmd(fields)
        elif fields[0] == "down":
        	down_cmd(fields)
        elif fields[0] == "up":
        	up_cmd(fields)
        elif fields[0] == "exit":
        	exit_cmd(fields)
        else: print("Unknown field", fields[0]);
        print()
    
    return 0 # currently unreachable code

if __name__ == '__main__':
    sys.exit( main() ) # run main function and then exit