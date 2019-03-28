# CHIP-8 Interpreter

---

| &nbsp;[![Build Status](https://travis-ci.org/IslayLaphroaig/CHIP-8.svg?branch=master)](https://travis-ci.org/IslayLaphroaig/CHIP-8)&nbsp;&nbsp; | &nbsp;&nbsp;[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)&nbsp;&nbsp; | &nbsp;&nbsp; [![code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)&nbsp;&nbsp; |
|-------|-------|-------|

---

![Breakout](/img/breakout.gif?raw=true)

## Description
This project is a CHIP-8 interpretor written in Python 3. The goal is to learn about the process of writing an interpreter/emulator while simultaneously learning about the Python programming language.

## License
The license is [MIT](https://github.com/IslayLaphroaig/CHIP-8/blob/master/LICENSE)

## Installation
The code was developed against Python 3.7.1 and was tested on Windows 10 and Manjaro Linux. Assuming Python 3.7 is installed and configured for your OS, clone the repository to a Python virtualenv or to another location of your choosing. Open a terminal and cd into the CHIP-8 directory, from here run "pip install -r requirements.txt". This will install glfw and PyOpenGL. To launch the interpreter, from the CHIP-8 directory, run "python .\src\main.py" which will open a file explorer using tkinter, navigate to a Chip-8 rom and open it to begin (make sure the rom has a .ch8 extension). No roms are currently provided, they are available on the internet.

Sound should work by default on Windows. For Linux and Mac you will need to install the sox package, refer to the documentation for that platform for installing sox.

## Key Mappings
The computers using the Chip-8 language had a 16-key hexadecimal keypad. The original keypad and the mappings which my Chip-8 interpreter uses is shown below:

	  Chip-8   Interpreter
	|1|2|3|C|   |1|2|3|4|
	|4|5|6|D|   |Q|W|E|R|
	|7|8|9|E|   |A|S|D|F|
	|A|0|B|F|   |Z|X|C|V|


## References
[Matthew Mikolay: Mastering Chip-8](http://mattmik.com/files/chip8/mastering/chip8.html)<br/>
[Laurence Muller: How to Write an Emulator (CHIP-8 Interpreter)](http://www.multigesture.net/articles/how-to-write-an-emulator-chip-8-interpreter/)<br/>
[Craig Thomas: Writing a Chip 8 Emulator](http://craigthomas.ca/blog/2014/06/21/writing-a-chip-8-emulator-part-1/)<br/>
[Cowgod's Chip-8 Technical Reference v 1.0](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM)<br/>
