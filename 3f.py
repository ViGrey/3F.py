#!/usr/bin/env python3

# Copyright (C) 2017, Vi Grey
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY AUTHOR AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

# A polyglot file generator, inspired by PoC||GTFO


import os.path
import sys

VERSION = "0.0.1"
FILE_EXTENSIONS = [[".zip"],
                   [".jpg", ".png", ".gif"],
                   [".pdf"]]


# Return True if the file has an extension in FILE_EXTENSIONS
def extension_valid(ext):
    global FILE_EXTENSIONS
    for file_set in FILE_EXTENSIONS:
        if ext in file_set:
            return True
    return False


# Check to make sure the input extensions are compatible for a polyglot file
def input_extensions_compare(ext1, ext2):
    global FILE_EXTENSIONS
    # Check to see if one of the input files is a ZIP file
    if ext1 in FILE_EXTENSIONS[0] or ext2 in FILE_EXTENSIONS[0]:
        # If both input files are a not a ZIP file
        if ext1 != ext2:
            return True
        print("\x1b[91mOnly one input can be a ZIP file\x1b[0m")
        return False
    print("\x1b[91mOne input must be a ZIP file\x1b[0m")
    return False


# Create the polyglot output file from the input file contents
def create_polyglot_file(content1, ext1, content2, ext2):
    global FILE_EXTENSIONS
    # If one of the inputs is an image file
    if ext1 in FILE_EXTENSIONS[1] or ext2 in FILE_EXTENSIONS[1]:
        # If the first input is the image file
        if ext1 not in FILE_EXTENSIONS[0]:
            # Append ZIP file contents to image file contents
            return(content1 + content2)
        # If the second input is the image file
        else:
            # Append ZIP file contents to image file contents
            return(content2 + content1)
    # Else if one of the inputs is a PDF
    else:
        # If the first input file is a PDF
        if ext1 in FILE_EXTENSIONS[2]:
            # Get endstream...%%EOF index of PDF file
            eof = content1.rfind(b"endstream")
            if eof != -1:
                # Append ZIP file contents to EOF stripped PDF and append the
                # EOF content at the end
                return(content1[:eof] + content2 + content1[eof:])
            else:
                print("\x1b[91mImproper PDF file format\x1b[0m")
                exit(1)
        # If the second input file is a PDF
        else:
            # Get endstream...%%EOF index of PDF file
            eof = content2.rfind(b"endstream")
            # If endstream...%%EOF index exists
            if eof != -1:
                # Append ZIP file contents to EOF stripped PDF and append the
                # EOF content at the end
                return(content2[:eof] + content1 + content2[eof:])
            else:
                print("\x1b[91mImproper PDF file format\x1b[0m")
                exit(1)
    print("\x1b[91mUnable to combine input files\x1b[0m")
    exit(1)

# Check if help or version flag was passed as an argument
if len(sys.argv) >= 2:
    if sys.argv[1] == "--help" or sys.argv[1] == "-h":
        print("Usage: python3 3f.py [ OPTIONS ] [ <input1_file> ] " +
              "[ <input2_file> ] [ <output_path> ]\n\n" +
              "Options:\n"
              "  -h, --help        Print Help (this message) and exit\n"
              "  -v, --version     Print version information and exit\n\n"
              "Examples:\n" +
              "  python3 3f.py a.zip b.png o.png\n" +
              "  python3 3f.py a.pdf b.zip o.pdf\n" +
              "  python3 3f.py a.gif b.zip o.zip")
        exit(0)
    elif sys.argv[1] == "--version" or sys.argv[1] == "-v":
        print("3F.py " + VERSION)
        exit(0)

# Close the program if 2 input files and an output path aren't given
if len(sys.argv) != 4:
    print("\x1b[91m2 input files and 1 output path required\x1b[0m")
    exit(1)

# Get the 2 inputs and 1 output values
input1 = sys.argv[1]
input2 = sys.argv[2]
output = sys.argv[3]

# Find extension of input1
input1_extension = os.path.splitext(input1)[1].lower()
if not extension_valid(input1_extension):
    print("\x1b[91mInvalid extention for first input file\x1b[0m")
    exit(1)

# Find extension of input2
input2_extension = os.path.splitext(input2)[1].lower()
if not extension_valid(input2_extension):
    print("\x1b[91mInvalid extention for second input file\x1b[0m")
    exit(1)

# Check to make sure the inputs have a cooperative set of extensions
if not input_extensions_compare(input1_extension, input2_extension):
    exit(1)

# Get contents of input files
try:
    input1_file = open(input1, "rb")
    input1_contents = input1_file.read()
    input1_file.close()
    input2_file = open(input2, "rb")
    input2_contents = input2_file.read()
    input2_file.close()
except:
    print("\x1b[91mUnable to open or read an input file\x1b[0m")
    exit(1)

# Create the output and write to the file
try:
    output_file = open(output, "wb+")
    output_file.write(create_polyglot_file(input1_contents, input1_extension,
                                           input2_contents, input2_extension))
    output_file.close()
except:
    print("\x1b[91mUnable to create or write output file\x1b[0m")
    exit(1)
