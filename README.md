# 3F.py - Frankenstein File Formatter

A polyglot file generator, inspired by PoC||GTFO

#### Dependencies:
- Python >= 3

#### Usage:
    python3 3f.py -h
    Usage: python3 3f.py [ OPTIONS ] [ <input1_file> ] [ <input2_file> ] [ <output_path> ]

    Options:
      -h, --help        Print Help (this message) and exit
      -v, --version     Print version information and exit

    Examples:
      python3 3f.py a.zip b.png o.png
      python3 3f.py a.pdf b.zip o.pdf
      python3 3f.py a.gif b.zip o.zip

#### Input File Types

One of the input files MUST be a ZIP file.  The other input file can either be a JPG/PNG/GIF image file or a PDF file.
