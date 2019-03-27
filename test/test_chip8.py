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


# load data into memory.
# load the font set at index 0 to test the data load process.
# the font set file contains the values noted in the Cowgod reference guide: http://devernay.free.fr/hacks/chip8/C8TECH10.HTM#2.4.
# assert that the values for index 0 and 79 match the values in the font set file, and that the next value is zero.
# assert that the index 0 to 79 are non-zero values and that index 80 onwards to the end of the memory array are zero values.
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


# bitwise operations.
# assert that the bitwise operations produce the correct values for each bitwise function using a dummy opcode value of 27138(0x6A02).
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


# clear the screen.
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


# return from a subroutine.
# assert that the stack pointer has been decremented by 1 and that the pc is set to the value of the stack at index 0.
def test_return_from_subroutine():
    chip_8 = Chip8()
    chip_8.stack[0] = 500
    chip_8.stack_pointer = 1
    chip_8.return_from_subroutine()
    assert chip_8.stack_pointer == 0
    assert chip_8.pc == 500


# jumpt to address at nnn.
# assert that the pc is set to the return value of the function nnn.
def test_jump_to_nnn():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    chip_8.jump_to_nnn()
    assert chip_8.pc == 2562


# call subroutine at nnn
# assert that the stack at index 0 (the vaulue of the stack pointer) is set to the value of the pc.
# assert that the stack pointer has been incremented by 1.
# assert that the pc is set to the return value of the function nnn.
def test_call_subroutine_at_nnn():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    chip_8.call_subroutine_at_nnn()
    assert chip_8.stack[0] == 512
    assert chip_8.stack_pointer == 1
    assert chip_8.pc == 2562


# skip next instruction if v[x] equals the return value of nn.
# assert that the return value of funcion x is equal to 10.
# assert that the return value of function nn is 2.
# set the value of v[10] to 2.
# assert that the pc has been incrememented by 2 as v[x] equals the return value of function nn.
def test_skip_if_vx_equals_nn():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    assert chip_8.x(chip_8.opcode) == 10
    assert chip_8.nn(chip_8.opcode) == 2
    chip_8.v[chip_8.x(chip_8.opcode)] = 2
    chip_8.skip_if_vx_equals_nn()
    assert chip_8.pc == 514


# skip the next instruction if v[x] does not equal the return value of nn.
# assert that the return value of funcion x is equal to 10.
# assert that the return value of function nn is 2.
# set the value of v[10] to 43.
# assert that the pc has been incrememented by 2 as v[x] does not equal the return value of function nn.
def test_skip_if_vx_not_equal_to_nn():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    assert chip_8.x(chip_8.opcode) == 10
    assert chip_8.nn(chip_8.opcode) == 2
    chip_8.v[chip_8.x(chip_8.opcode)] = 43
    chip_8.skip_if_vx_not_equal_to_nn()
    assert chip_8.pc == 514


# skip the next instruction if v[x] equals v[y].
# assert that the return value of funcion x is equal to 11.
# assert that the return value of function y is equal to 11.
# assert that the pc has been incremented by 2 as v[x] equals v[y].
def test_skip_if_vx_equals_vy():
    chip_8 = Chip8()
    chip_8.opcode = 3000
    assert chip_8.x(chip_8.opcode) == 11
    assert chip_8.y(chip_8.opcode) == 11
    chip_8.skip_if_vx_equals_vy()
    assert chip_8.pc == 514


# set v[x] to nn.
# assert that the return value of funcion x is equal to 10.
# assert that the return value of function nn is equal to 2.
# assert that v[x] has been set to the return value of function nn.
def test_set_vx_to_nn():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    assert chip_8.x(chip_8.opcode) == 10
    assert chip_8.nn(chip_8.opcode) == 2
    chip_8.set_vx_to_nn()
    assert chip_8.v[10] == 2


# add the value of nn to the value in v[x].
# assert that the return value of funcion x is equal to 10.
# assert that the return value of function nn is equal to 2.
# assert that the value of v[x] is equal to the value in v[x] plus the return value of the function nn.
def test_set_vx_to_vx_plus_nn():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    assert chip_8.x(chip_8.opcode) == 10
    assert chip_8.nn(chip_8.opcode) == 2
    chip_8.v[10] = 23
    chip_8.set_vx_to_vx_plus_nn()
    assert chip_8.v[10] == 25


# set v[x] to the value of v[y].
# assert that the return value of funcion x is equal to 10.
# assert that the return value of function y is equal to 0.
# assert that the value of v[x] has been set to the value of v[y].
def test_set_vx_to_vy():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    assert chip_8.x(chip_8.opcode) == 10
    assert chip_8.y(chip_8.opcode) == 0
    chip_8.v[10] = 12
    chip_8.v[0] = 3
    chip_8.set_vx_to_vy()
    assert chip_8.v[10] == 3


# set v[x] to v[x] OR v[y].
# assert that the return value of funcion x is equal to 10.
# assert that the return value of function y is equal to 0.
# assert that the value of v[x] has been set to the bitwise OR operation between the values in v[x] and v[y].
def test_set_vx_to_vx_or_vy():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    assert chip_8.x(chip_8.opcode) == 10
    assert chip_8.y(chip_8.opcode) == 0
    chip_8.v[10] = 23
    chip_8.v[0] = 44
    chip_8.set_vx_to_vx_or_vy()
    assert chip_8.v[10] == 63


# set v[x] to v[x] AND v[y].
# assert that the return value of funcion x is equal to 10.
# assert that the return value of function y is equal to 0.
# assert that the value of v[x] has been set to the bitwise AND operation between the values in v[x] and v[y].
def test_set_vx_to_vx_and_vy():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    assert chip_8.x(chip_8.opcode) == 10
    assert chip_8.y(chip_8.opcode) == 0
    chip_8.v[10] = 23
    chip_8.v[0] = 44
    chip_8.set_vx_to_vx_and_vy()
    assert chip_8.v[10] == 4


# set v[x] to v[x] XOR v[y].
# assert that the return value of funcion x is equal to 10.
# assert that the return value of function y is equal to 0.
# assert that the value of v[x] has been set to the bitwise XOR operation between the values in v[x] and v[y].
def test_set_vx_to_vx_xor_vy():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    assert chip_8.x(chip_8.opcode) == 10
    assert chip_8.y(chip_8.opcode) == 0
    chip_8.v[10] = 23
    chip_8.v[0] = 44
    chip_8.set_vx_to_vx_xor_vy()
    assert chip_8.v[10] == 59


# set v[x] to v[x] plus v[y], v[F] is set 0 when there is no carry.
# assert that the return value of funcion x is equal to 10.
# assert that the return value of function y is equal to 0.
# assert that there is no carry.
# assert that the value of v[x] is set to v[x] plus v[y].
def test_set_vx_to_vx_plus_vy_no_carry():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    assert chip_8.x(chip_8.opcode) == 10
    assert chip_8.y(chip_8.opcode) == 0
    chip_8.v[10] = 23
    chip_8.v[0] = 44
    chip_8.set_vx_to_vx_plus_vy()
    assert chip_8.v[0xF] == 0
    assert chip_8.v[10] == 67


# set v[x] to v[x] plus v[y], v[F] is set to 1 when there is a carry.
# assert that the return value of funcion x is equal to 10.
# assert that the return value of function y is equal to 0.
# assert that there is a carry.
# assert that the value of v[x] is set to v[x] plus v[y].
def test_set_vx_to_vx_plus_vy_carry():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    assert chip_8.x(chip_8.opcode) == 10
    assert chip_8.y(chip_8.opcode) == 0
    chip_8.v[10] = 254
    chip_8.v[0] = 143
    chip_8.set_vx_to_vx_plus_vy()
    assert chip_8.v[0xF] == 1
    assert chip_8.v[10] == 141


# set v[x] to v[x] minus v[y], v[F] is set to 0 when there is a borrow.
# assert that the return value of funcion x is equal to 10.
# assert that the return value of function y is equal to 0.
# assert that there is a borrow.
# assert that the value of v[x] is set to v[x] minus v[y].
def test_set_vx_to_vx_minus_vy_borrow():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    assert chip_8.x(chip_8.opcode) == 10
    assert chip_8.y(chip_8.opcode) == 0
    chip_8.v[10] = 23
    chip_8.v[0] = 44
    chip_8.set_vx_to_vx_minus_vy()
    assert chip_8.v[0xF] == 0
    assert chip_8.v[10] == 235


# set v[x] to v[x] minus v[y], v[F] is set to 1 when there is no borrow.
# assert that the return value of funcion x is equal to 10.
# assert that the return value of function y is equal to 0.
# assert that there is no borrow.
# assert that the value of v[x] is set to v[x] minus v[y].
def test_set_vx_to_vx_minus_vy_no_borrow():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    assert chip_8.x(chip_8.opcode) == 10
    assert chip_8.y(chip_8.opcode) == 0
    chip_8.v[10] = 254
    chip_8.v[0] = 143
    chip_8.set_vx_to_vx_minus_vy()
    assert chip_8.v[0xF] == 1
    assert chip_8.v[10] == 111


# store least significant bit of v[x] in v[F] and shift v[x] to the right by one.
# assert that the return value of funcion x is equal to 10.
# assert that the value of v[x] has been shifted right by one.
# assert that the least significant bit of v[x] is stored in v[F].
def test_set_vx_to_vx_shr_1():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    assert chip_8.x(chip_8.opcode) == 10
    chip_8.v[10] = 11
    chip_8.set_vx_to_vx_shr_1()
    assert chip_8.v[10] == 5
    assert chip_8.v[0xF] == 1


# set v[x] to v[y] minus v[x], v[F] is set to 1 when there is no borrow.
# assert that the return value of funcion x is equal to 10.
# assert that the return value of funcion y is equal to 0.
# assert that there is no borrow.
# assert that the value of v[x] is set to v[y] minus v[x].
def test_set_vx_to_vy_minus_vx_no_borrow():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    assert chip_8.x(chip_8.opcode) == 10
    assert chip_8.y(chip_8.opcode) == 0
    chip_8.v[10] = 23
    chip_8.v[0] = 44
    chip_8.set_vx_to_vy_minus_vx()
    assert chip_8.v[0xF] == 1
    assert chip_8.v[10] == 21


# set v[x] to v[y] minus v[x], v[F] is set to 0 when there is a borrow.
# assert that the return value of funcion x is equal to 10.
# assert that the return value of funcion y is equal to 0.
# assert that there is no borrow.
# assert that the value of v[x] is set to v[y] minus v[x].
def test_set_vx_to_vy_minus_vx_borrow():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    assert chip_8.x(chip_8.opcode) == 10
    assert chip_8.y(chip_8.opcode) == 0
    chip_8.v[10] = 254
    chip_8.v[0] = 143
    chip_8.set_vx_to_vy_minus_vx()
    assert chip_8.v[0xF] == 0
    assert chip_8.v[10] == 145


# store most significant bit of v[x] in v[F] and shift v[x] to the left by one.
# assert that the return value of funcion x is equal to 10.
# assert that the value of v[x] has been shifted left by one.
# assert that the most significant bit of v[x] is stored in v[F].
def test_set_vx_to_vx_shl_1():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    assert chip_8.x(chip_8.opcode) == 10
    chip_8.v[10] = 200
    chip_8.set_vx_to_vx_shl_1()
    assert chip_8.v[10] == 400
    assert chip_8.v[0xF] == 1


# # skip the next instruction if v[x] does not equal v[y].
# assert that the return value of funcion x is equal to 10.
# assert that the return value of funcion y is equal to 0.
# assert that the pc has been incremented by 2 as v[x] does not equal v[y].
def test_skip_if_vx_not_equal_vy():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    assert chip_8.x(chip_8.opcode) == 10
    assert chip_8.y(chip_8.opcode) == 0
    chip_8.skip_if_vx_equals_vy()
    assert chip_8.pc == 514


# set i to address nnn.
# assert that 16 bit register i is set to the address nnn.
def test_set_i_to_nn():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    chip_8.set_i_to_nn()
    assert chip_8.i == 2562


# jump to address nnn plus v[0].
# assert that the pc is now set to nnn plus v[0].
def test_jump_to_nnn_plus_v0():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    chip_8.v[0x0] = 8
    chip_8.jump_to_nnn_plus_v0()
    assert chip_8.pc == 2570


# skip next instruction of the key stored in v[x] is pressed.
# assert that the pc has been incrememented by 2 if the value of x[x] is 1.
def test_skip_if_key_equals_vx():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    chip_8.keys[chip_8.v[chip_8.x(chip_8.opcode)]] = 1
    chip_8.skip_if_key_equals_vx()
    assert chip_8.pc == 514


# skip next instruction of the key stored in v[x] is not pressed.
# assert that the pc has been incrememented by 2 if the value of x[x] is 0.
def test_skip_if_key_not_equal_to_vx():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    chip_8.keys[chip_8.v[chip_8.x(chip_8.opcode)]] = 0
    chip_8.skip_if_key_not_equal_to_vx()
    assert chip_8.pc == 514


# set v[x] to the value of the delay timer.
# assert that the return value of funcion x is equal to 10.
# assert that the value of v[x] is set to the value of the delay timer.
def test_set_vx_to_delay_timer():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    chip_8.delay_timer = 1
    assert chip_8.x(chip_8.opcode) == 10
    chip_8.set_vx_to_delay_timer()
    assert chip_8.v[10] == 1


# store key press in v[x].
# assert that the pc remains the same.
def test_store_keypress_in_vx_key_pressed():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    chip_8.keys[3] = 1
    chip_8.store_keypress_in_vx()
    assert chip_8.pc == 512


# store key press in v[x].
# # assert that the pc has been decremented by 2 as no key has been pressed.
def test_store_keypress_in_vx_no_key_pressed():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    chip_8.store_keypress_in_vx()
    assert chip_8.pc == 510


# set delay timer to v[x].
# assert that the return value of funcion x is equal to 10.
# assert that the delay timer is set to the value of v[x].
def test_set_delay_timer_to_vx():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    assert chip_8.x(chip_8.opcode) == 10
    chip_8.v[10] = 1
    chip_8.set_delay_timer_to_vx()
    assert chip_8.delay_timer == 1


# set sound timer to v[x].
# assert that the return value of funcion x is equal to 10.
# assert that the sound timer is set to the value of v[x].
def test_set_sound_timer_to_vx():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    assert chip_8.x(chip_8.opcode) == 10
    chip_8.v[10] = 1
    chip_8.set_sound_timer_to_vx()
    assert chip_8.sound_timer == 1


# set i to i plus v[x].
# assert that the return value of funcion x is equal to 10.
# assert that i is set to i plus v[x].
def test_set_i_to_i_plus_vx():
    chip_8 = Chip8()
    chip_8.opcode = 27138
    assert chip_8.x(chip_8.opcode) == 10
    chip_8.v[10] = 23
    chip_8.set_i_to_i_plus_vx()
    assert chip_8.i == 23