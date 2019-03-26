import pytest
from src.chip8 import Chip8


# assert the constructor initialises the variable values and array lengths correctly.
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
# assert that the values for index 0 and 79 match the values in the font set file, and that the next value is a zero value.
# assert that the index 0 to 79 are non-zero values and that index 80 onwards to the end of the memory array is non-zero values.
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


# tests for the bitwise operations using an opcode value of 27138.
# assert that the bitwise operations produce the correct values.
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
# clear the screen and assert that all of the values have been reset to 0.
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
# assert that the stack pointer has been decremented by 1 and that the pc is set to the value of the stack at index 0
def test_return_from_subroutine():
    chip_8 = Chip8()
    chip_8.stack[0] = 500
    chip_8.stack_pointer = 1
    chip_8.return_from_subroutine()
    assert chip_8.stack_pointer == 0
    assert chip_8.pc == 500


# calling jump_to_nnn sets the pc to the return value of the bitwise nnn operation which takes an opcode as a parameter.
# assert that the pc is set to the return value of the bitwise operation nnn
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


# the bitwise operations for opcode 2562 will result in index 10 of the v register.
# therefore set the value of this register to 2 as the bitwise operation for self.nn(self.opcode) will return the value of 2.
# assert that the program counter has been incremented correctly by 2 if the values are equal.
def test_skip_if_vx_equals_nn():
    chip_8 = Chip8()
    chip_8.opcode = 2562
    assert chip_8.x(chip_8.opcode) == 10
    assert chip_8.nn(chip_8.opcode) == 2
    chip_8.v[chip_8.x(chip_8.opcode)] = 2
    chip_8.skip_if_vx_equals_nn()
    assert chip_8.pc == 514

# the bitwise operations for opcode 2562 will result in index 10 of the v register.
# therefore set the value of this register to 43 to ensure they are not equal as the bitwise operation for self.nn(self.opcode) will return the value of 2.
# assert that the program counter has been incremented correctly by 2 if the values are not equal.
def test_skip_if_vx_not_equal_to_nn():
    chip_8 = Chip8()
    chip_8.opcode = 2562
    assert chip_8.x(chip_8.opcode) == 10
    assert chip_8.nn(chip_8.opcode) == 2
    chip_8.v[chip_8.x(chip_8.opcode)] = 43
    chip_8.skip_if_vx_not_equal_to_nn()
    assert chip_8.pc == 514


# the bitwise operations for x and y should both return 11.
# assert that if the two values are equal that the pc is incremented by 2.
def test_skip_if_vx_equals_vy():
    chip_8 = Chip8()
    chip_8.opcode = 3000
    assert chip_8.x(chip_8.opcode) == 11
    assert chip_8.y(chip_8.opcode) == 11
    chip_8.skip_if_vx_equals_vy()
    assert chip_8.pc == 514


# the bitwise operations for opcode 2562 will result in index 10 of the v register.
# assert that the value of this register is set to the value of the bitwise operation for nn.
def test_set_vx_to_nn():
    chip_8 = Chip8()
    chip_8.opcode = 2562
    assert chip_8.x(chip_8.opcode) == 10
    assert chip_8.nn(chip_8.opcode) == 2
    chip_8.set_vx_to_nn()
    assert chip_8.v[10] == 2


# the bitwise operations for opcode 2562 will result in index 10 of the v register.
# the value of this register should then be set to the value of the bitwise operation for nn.
# the value of index 10 is set to the dummy value of 23 in order to add the value of nn to it.
# the modulo keeps the value within the 8 bit range.
# assert that index 10 of v is set to 25.
def test_set_vx_to_vx_plus_nn():
    chip_8 = Chip8()
    chip_8.opcode = 2562
    assert chip_8.x(chip_8.opcode) == 10
    assert chip_8.nn(chip_8.opcode) == 2
    chip_8.v[10] = 23
    chip_8.set_vx_to_vx_plus_nn()
    assert chip_8.v[10] == 25


# the bitwise operations of x for opcode 2562 will result in index 10 of the v register.
# the bitwise operations of y for opcode 2562 will result in index 0 of the v register.
# dummy values for the registers are then set.
# assert that the value of register 10 is now eplaced by the value in register 0.
def test_set_vx_to_vy():
    chip_8 = Chip8()
    chip_8.opcode = 2562
    assert chip_8.x(chip_8.opcode) == 10
    assert chip_8.y(chip_8.opcode) == 0
    chip_8.v[10] = 12
    chip_8.v[0] = 3
    chip_8.set_vx_to_vy()
    assert chip_8.v[10] == 3