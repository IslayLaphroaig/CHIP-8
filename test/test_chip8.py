import pytest
from src.chip8 import Chip8


chip_8 = Chip8()


# ensure the constructor initialises the values and array lengths correctly.
def test_consutructor():
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
# the remaining values for the memory should be zero, therefore we check that the memory is filled with non-zero values for index 0 to 79 and 0 values for the remainder of the memory
def test_load_data():
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
