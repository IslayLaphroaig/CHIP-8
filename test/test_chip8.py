import pytest
from src.chip8 import Chip8


# ensure the constructor initialises the variable values and array lengths correctly.
def test_consutructor():
    chip_8 = Chip8()
    assert chip_8.opcode == 0
    assert len(chip_8.memory) == 4096
    assert len(chip_8.v) == 16
    assert chip_8.i == 0
    assert chip_8.pc == 512
    assert len(chip_8.stack) == 16
    assert chip_8.stack_pointer == 0
    assert chip_8.delay_timer == 0
    assert chip_8.sound_timer == 0
    assert len(chip_8.display) == 2048
    assert chip_8.draw_flag == False
    assert chip_8.play_sound == False


# load the font set at index 0 to test the data load process.
# the font set file contains the values noted in the Cowgod reference guide: http://devernay.free.fr/hacks/chip8/C8TECH10.HTM#2.4.
# the remaining values for the memory should be zero, therefore we check that the memory is filled with non-zero values for index 0 to 79 and zero values for the remainder of the memory.
def test_load_data():
    chip_8 = Chip8()
    chip_8.load_data("font_set", 0)

    assert chip_8.memory[0] == 240
    assert chip_8.memory[79] == 128
    assert chip_8.memory[80] == 0

    i = 0
    while i < 80:
        assert chip_8.memory[i] > 0
        i += 1

    j = 80
    while j < len(chip_8.memory):
        assert chip_8.memory[j] == 0
        j += 1

# tests for the bitwise operatorations using an opcode value of 27138.
def test_nnn():
    chip_8 = Chip8()
    opcode = 27138
    assert chip_8.nnn(opcode) == 2562


def test_nn():
    chip_8 = Chip8()
    opcode = 27138
    assert chip_8.nn(opcode) == 2


def test_n():
    chip_8 = Chip8()
    opcode = 27138
    assert chip_8.n(opcode) == 2


def test_x():
    chip_8 = Chip8()
    opcode = 27138
    assert chip_8.x(opcode) == 10


def test_y():
    chip_8 = Chip8()
    opcode = 27138
    assert chip_8.y(opcode) == 0

# fill all of the display elements with values of 1.
# clear the screen and ensure all of the values have been reset to 0.
def test_clear_screen():
    chip_8 = Chip8()
    i = 0
    while i < len(chip_8.display):
        chip_8.display[i] += 1
        i += 1
    
    chip_8.clear_screen()

    assert len(chip_8.display) == 2048
    
    i = 0
    while i < len(chip_8.display):
        assert chip_8.display[i] == 0
        i += 1

# set index 0 of the stack to 500.
# set the stack pointer to 1 so that when return_from_subroutine is called the stackpointer should be decremented by 1 to 0.
# if the stack pointer is decremented by one then this should set the pc to the value of the first elemement of the stack, which we have set to 500.
def test_return_from_subroutine():
    chip_8 = Chip8()
    chip_8.stack[0] = 500
    chip_8.stack_pointer = 1

    chip_8.return_from_subroutine()
    assert chip_8.stack_pointer == 0
    assert chip_8.pc == 500


# calling jump_to_nnn sets the pc to the return value of the bitwise nnn operation which takes an opcode as a parameter.
def test_jump_to_nnn():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    chip_8.jump_to_nnn()
    assert chip_8.pc == 2562


# calling call_subroutine_at_nnn passes the stack pointer as an index to the stack, and sets this index to the value of the pc.
# the stack pointer is then incremented by 1.
# the pc is then set to the return value of the bitwise nnn operation which takes an opcode as a parameter.
def test_call_subroutine_at_nnn():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    chip_8.call_subroutine_at_nnn()
    assert chip_8.stack[0] == 512
    assert chip_8.stack_pointer == 1
    assert chip_8.pc == 2562