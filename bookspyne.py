#!/usr/bin/env python

from typing import *
from os import mkdir
from os import listdir
from os.path import isfile, join
from sys import argv

""" #@
@name: Introduction
@notes: 
Bookspyne is a tool written in python that can be used to merge multiple Markdown files together and create a table of contents for them.
The tool will automatically get all the headers of the file and list them, automatically creating a link that will bring to the specified paragraph or section for each of them.
Here's how it works:
There are two ways to use this tool

### 1 Using a Table of Contents file
Create a normal txt (or md) file (the name is not important) structured as follows:
```
title: {Title}
{filename1}
...
{filenameN}
```
where the string that follows "title:" will be used as a title assigned to the merged files (it will appear with a bigger font and centerd)
and each new line shows a file that will be merged in the completed document.

**After moving in the directory where the file "bookspyne.py" was created**, type in the console:
```console
python bookspyne.py -i {toc_file}.txt -o {output_filename}.md
```
where the {toc_file}.txt file is the Table of contents file created previously and the {output_filename} is the filename of the output file containing all the merged files.

### 2 Using a Source Directory
In this case, specify the directory where all the files that will be merged are located, then use the following command:
```console
python bookspyne.py --fromdir {source_directory} -t {Title}
```
the command will use the {source_directory} path to get all the files needed and the {Title}, as you might have guessed, as a title for the whole document.

# Installing the tool
If PIP is installed on your machine, you can clone this repository and use the following command:
```console
pip install -e {cloned repo directory path}
```
this will enable the use of the command without specifying the environment and the file path, just by using `bookspyne`:
```console
bookspyne -i {toc_file}.txt -o {output_filename}.md
```
will be equivalent as:
```console
python bookspyne.py -i {toc_file}.txt -o {output_filename}.md
```
@# """

""" #@
@name: print_usage
@notes: prints the usage of the tool
@inputs:
- None
@outputs:
None
@# """
def print_usage():
    print(
"""Usage:
    -o: output file title
    -i: input file title
    -t: title of the completed file
    --fromdir: source directory base
    --usage: prints usage information
Example usage:
python bookspyne.py -i {toc_file}.txt -o {output_file}.md

from this command, a file named {output_file}.md will be created containing
the files listed in the {toc_file}.txt (as explained below) all merged together
with an automatic table of content

Using: 
python bookspyne.py
is equivalent to:
python bookspyne.py -i ./toc.txt -o ./out/out.md

Example usage:
python bookspyne.py --fromdir {dir_path} -t {Title} -o {output_file}.md

from this command, a file named {output_file}.md will be created containing
all the files in the specified {dir_path} directory sorted by name all merged 
together with an automatic table of content title with the string "{Title}"

The -t flag is madatory if the --fromdir flag is used, while it will be ignored
if the -i argument is used

How to create a Table Of Content file:
- create a .txt file
- within it define:
    - a title with the string "title: {title}".
    - in a new line for each, add the path of 
    the files that will be merged together

Table of Content file Example:
title: Example
./file1.md
./file2.md
...
./lastfile.md

from this Table of Content file the file that will be created
will have as title the string "Example" and as contents 
the contents of the listed files in the listed order.
""")



""" #@
@name: extract_data
@brief: extractes the data from the files
@notes: given all the informations reguarding the files that have to be merged, the method will automatically extract the contents of the files (sorted by name in case of source directory)
@inputs: 
- str path: table of contents file path or source directory path
- bool directory: wether the path is a directory or a file
- str title: title specified in case a source directory is used
@outputs: 
- Tuple[str, List[str]]: contains the title and the list of contents of the file
@# """
def extract_data(path: str, directory: bool = False, title: str =  None) -> Tuple[str, List[str]]:
    data: List[str] = []
    book_title: str = ""
    files_list: str = []

    if not directory:
        try:
            # if a file was specified
            with open(path, "r") as index_files:
                data = index_files.readlines()
                book_title = ":".join(data[0].split(":")[1:])
                files_list = data[1:] # create a file list from the contents of the table of contents file
        except(FileNotFoundError):
            print(f"{path} file was not found")
    else:
        # list all the files in the source directory
        files_list = sorted(["/".join([path,f]) for f in listdir(path) if isfile(join(path, f))])
        book_title = title

    data = []
    for file_name in files_list:
        with open(file_name.strip(), "r") as file_data:
            # read each of the specified files
            data += file_data.readlines() 
            #? maybe loading all these files in the main memory is not a good move, 
            #? maybe modify to handle each file separately and append info to the 
            #? output file as it goes?
    return (book_title, data)


""" #@
@name: format_toc_item
@brief: formats an item of the table of document
@notes: uses the number of "#" symbols as the number of tabulations that will be inserted, to specify how deep in the list this item should go
@inputs: 
- str toc_item: item to be insterted in the table of contents
- str id: id, used for linking
@outputs: 
- str: formatted item
@# """
def format_toc_item(toc_item: str, id: str) ->str:
    toc_item_data = toc_item.split(" ")
    first_part = toc_item_data[0]+" " # get the "#" symbols
    second_part = " ".join(toc_item_data[1:]).strip() # get the header contents
    first_part = first_part.replace("# ", "-")
    first_part = first_part.replace("#", "\t")
    return f"{first_part}  [{second_part}](#{id})"


""" #@
@name: create_bookspine
@brief: merges all the files together and adds a table of content
@notes: given the file data it creates a table of contents and then merges all the files together
@inputs: 
- str book_title: title of the whole merged data
- str book_data: contents of the file
@outputs: 
- str: stirng that has to bre written in the putput file
@# """
def create_bookspine(book_title: str, book_data: str) -> str:
    whole_data = ""
    # use html to format the title
    formatted_title: str = "<div style=\"margin:auto;" +\
        " padding:auto; width:100%; text-align:center;" +\
        f" font-size:48px\">{book_title.strip()}</div>\n"
    toc: str = ""
    for line in book_data:
        if line[0] == "#":  # found a title
            # create the section id and then format the toc item
            section_title = line.strip()
            section_id = "-".join(line.split(" ")[1:]).lower().strip()
            # add the toc item to the toc and add the line as it is to the output file
            toc += "\n" + format_toc_item(section_title, section_id)
            whole_data += f"\n\n\n{section_title.strip()}\n"
            continue
        whole_data += line # add the line as it is to the file
    return "\n".join([formatted_title + toc + whole_data])

""" #@
@name: handle_inputs
@brief: handles the input arguments of the command
@notes: the method takes the input arguments and then uses the `extract_data` and `create_bookspine` method to merge all the files together with a table of contents
@inputs: 
- None
@outputs: 
- None
@# """
def handle_inputs() -> None:
    # default values
    toc_path: str = "./toc.txt"
    file_name: str = "./out.md"
    source_directory: bool = False
    title: str = None
    # handle the arguments
    i: int = 1
    while i < len(argv):
        argument = argv[i]
        match argument:
            case "-o":
                i = i+1
                file_name = argv[i]
            case "-i":
                i = i+1
                toc_path = argv[i]
            case "-t":
                i = i+1
                title = argv[i]
            case "--fromdir":
                i = i+1
                toc_path = argv[i]
                source_directory = True
            case "--usage":
                print_usage()
                return None
            case default:
                print(f"Unknown flag or argument {argument},\nUse --usage for usage instructions")
                return None
        i = i+1

    book: str = ""
    if source_directory :
        if not title:
            print("Missing Title, specify it with the -t flag")
            return
    (book_title, data) = extract_data(toc_path, directory=source_directory, title=title)
    book = create_bookspine(book_title, data)
    # if the file_name contains directories
    path_list:List[str] = file_name.split("/")
    directory: str = ""
    for path_dir in path_list[:len(path_list)-1]:
        # create the directory it it does not exist
        try:
            directory += path_dir + "/"
            mkdir(directory)
        except(FileExistsError):
            continue
    # write the output file
    with open(file_name, "w") as created_file:
        created_file.write(book)

