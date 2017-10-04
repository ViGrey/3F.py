#!/usr/bin/env python3

# Copyright (C) 207, Vi Grey
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

import sys

if len(sys.argv) != 4:
  print("2 input files and 1 output path required")
  exit(1)

# Test for file extensions of input files
i1 = sys.argv[1]
if i1.rfind('.') != len(i1) - 4:
  print("Invalid extention for first input file")
  exit(1)
i1ext = i1[i1.rfind('.') + 1:].lower()

i2 = sys.argv[2]
if i2.rfind('.') != len(i2) - 4:
  print("Invalid extention for first input file")
  exit(1)
i2ext = i2[i2.rfind('.') + 1:].lower()

o = sys.argv[3]

if i1ext in ['jpg', 'png', 'gif'] and i2ext in ['jpg', 'png', 'gif']:
  print("One input must be a zip file")
  exit(1)
elif i1ext == 'pdf' and i2ext == 'pdf':
  print("One input must be a zip file")
  exit(1)
elif i1ext == 'zip' and i2ext == 'zip':
  print("Unable to combine 2 zip files")
  exit(1)
elif not (i1ext in ['jpg', 'png', 'gif', 'pdf', 'zip'] and
          i2ext in ['jpg', 'png', 'gif', 'pdf', 'zip'] and
          (i1ext == 'zip' or i2ext == 'zip')):
  print("Unable to combine input files")
  exit(1)

try:
  in1 = open(i1, "rb")
  i1contents = in1.read()
  in1.close()
except:
  print("Unable to open first input file")
  exit(1)

try:
  in2 = open(i2, "rb")
  i2contents = in2.read()
  in2.close()
except:
  print("Unable to open second input file")
  exit(1)

try:
  out = open(o, "wb+")
  if i1ext in ['jpg', 'png', 'gif'] or i2ext in ['jpg', 'png', 'gif']:
    if i1ext != 'zip':
      out.write(i1contents + i2contents)
      print(len(i1contents + i2contents))
      out.close()
    else:
      out.write(i2contents + i1contents)
  elif i1ext == 'pdf' or i2ext == 'pdf':
    if i1ext == 'pdf':
      eof = i1contents.rfind(b'endstream')
      if eof != -1:
        out.write(i1contents[:eof] + i2contents + i1contents[eof:])
      else:
        print("Improper PDF file format")
        exit(1)
    else:
      eof = i2contents.rfind(b'endstream')
      if eof != -1:
        out.write(i2contents[:eof] + i1contents + i2contents[eof:])
      else:
        print("Improper PDF file format")
        exit(1)
except:
  print("Unable to create or write output file")
  exit(1)
