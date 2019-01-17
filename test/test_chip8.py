import pytest
from src.chip8 import Chip8

chip_8 = Chip8()

# example test for setting up initial testing framework
def test_I():
    assert(chip_8.I == 0)