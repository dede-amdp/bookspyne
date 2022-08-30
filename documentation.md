# Bookspyne


## Introduction

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

 

---

## print_usage

prints the usage of the tool
### Inputs
- None

### Outputs
None
 

---

## extract_data
> extractes the data from the files

given all the informations reguarding the files that have to be merged, the method will automatically extract the contents of the files (sorted by name in case of source directory)
### Inputs
- str path: table of contents file path or source directory path
 - bool directory: wether the path is a directory or a file
 - str title: title specified in case a source directory is used

### Outputs
- Tuple[str, List[str]]: contains the title and the list of contents of the file
 

---

## format_toc_item
> formats an item of the table of document

uses the number of "#" symbols as the number of tabulations that will be inserted, to specify how deep in the list this item should go
### Inputs
- str toc_item: item to be insterted in the table of contents
 - str id: id, used for linking

### Outputs
- str: formatted item
 

---

## idfy
> creates id from section title

strips the section title of all the non alphanumeric characters to always have a valid link
### Inputs
- str id_str: string of the title without the "#" characters

### Outputs
- str: id of the section
 

---

## create_bookspine
> merges all the files together and adds a table of content

given the file data it creates a table of contents and then merges all the files together
### Inputs
- str book_title: title of the whole merged data
 - str book_data: contents of the file

### Outputs
- str: stirng that has to bre written in the putput file
 

---

## handle_inputs
> handles the input arguments of the command

the method takes the input arguments and then uses the `extract_data` and `create_bookspine` method to merge all the files together with a table of contents
### Inputs
- None

### Outputs
- None
 

---
---

generated with [EasyGen](http://easygen.altervista.org/) - [On Github](https://github.com/dede-amdp/easygen).