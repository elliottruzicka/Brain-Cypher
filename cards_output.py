import os
from FileData import FileData


def setup():
    filePath = os.getcwd() + "/temp_output.txt"
    file = FileData(filePath)
    return filePath, file


def print_file(filePath):
    import subprocess

    subprocess.call(["notepad.exe", '/p', filePath])  # Open the output file with the instruction to print


def start(printString):
    filePath, file = setup()  # Set up output file

    file.write_file(printString)  # Write the string to the output file

    print_file(filePath)  # Print the file

    # overwrite file data in readwrite mode
    file.overwrite_file("##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################\n"
                        "##############################")

    os.remove(filePath)  # Deletes the output file
