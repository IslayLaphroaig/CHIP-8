from random import random

DISPLAY_HEIGHT = 32
DISPLAY_WIDTH = 64


class Chip8:
    def __init__(self):
        self.opcode = 0
        self.first_four_bits_of_opcode = 0
        self.decoded_opcode = 0
        self.memory = [0] * 4096
        self.v = [0] * 16
        self.i = 0
        self.pc = 512
        self.stack = [0] * 16
        self.stack_pointer = 0
        self.delay_timer = 0
        self.sound_timer = 0
        self.keys = [0] * 16
        self.display = [0] * (64 * 32)
        self.draw_flag = False

    def load_data(self, file, offset):
        data = open(file, "rb").read()
        for index, byte in enumerate(data):
            self.memory[offset + index] = byte

    def update_timers(self):
        if self.delay_timer > 0:
            self.delay_timer -= 1

        if self.sound_timer > 0:
            self.sound_timer -= 1

    def nnn(self, opcode):
        return opcode & 0x0FFF

    def nn(self, opcode):
        return opcode & 0x00FF

    def n(self, opcode):
        return opcode & 0x000F

    def x(self, opcode):
        return (opcode & 0x0F00) >> 8

    def y(self, opcode):
        return (opcode & 0x00F0) >> 4

    def clear_screen(self):
        self.display = [0] * (64 * 32)
        self.draw_flag = True

    def return_from_subroutine(self):
        self.stack_pointer -= 1
        self.pc = self.stack[self.stack_pointer]

    def jump_to_nnn(self):
        self.pc = self.nnn(self.opcode)

    def call_subroutine_at_nnn(self):
        self.stack[self.stack_pointer] = self.pc
        self.stack_pointer += 1
        self.pc = self.nnn(self.opcode)

    def skip_if_vx_equals_nn(self):
        if self.v[self.x(self.opcode)] == self.nn(self.opcode):
            self.pc += 2

    def skip_if_vx_not_equal_to_nn(self):
        if not self.v[self.x(self.opcode)] == self.nn(self.opcode):
            self.pc += 2

    def skip_if_vx_equals_vy(self):
        if not self.v[self.x(self.opcode)] == self.nn(self.opcode):
            self.pc += 2

    def set_vx_to_nn(self):
        self.v[self.x(self.opcode)] = self.nn(self.opcode)

    def set_vx_to_vx_plus_nn(self):
        self.v[self.x(self.opcode)] += self.nn(self.opcode)
        self.v[self.x(self.opcode)] %= 256

    def set_vx_to_vy(self):
        self.v[self.x(self.opcode)] = self.v[self.y(self.opcode)]

    def set_vx_to_vx_or_vy(self):
        self.v[self.x(self.opcode)] = (
            self.v[self.x(self.opcode)] | self.v[self.y(self.opcode)]
        )

    def set_vx_to_vx_and_vy(self):
        self.v[self.x(self.opcode)] = (
            self.v[self.x(self.opcode)] & self.v[self.y(self.opcode)]
        )

    def set_vx_to_vx_xor_vy(self):
        self.v[self.x(self.opcode)] = (
            self.v[self.x(self.opcode)] ^ self.v[self.y(self.opcode)]
        )

    def set_vx_to_vx_plus_vy(self):
        self.v[0xF] = [0x0]
        total = self.v[self.x(self.opcode)] + self.v[self.y(self.opcode)]
        if total > 255:
            self.v[0xF] = [0x1]
            total -= 256
        self.v[self.x(self.opcode)] = total

    def set_vx_to_vx_minus_vy(self):
        self.v[0xF] = [0x1]
        difference = self.v[self.x(self.opcode)] - self.v[self.y(self.opcode)]
        if difference < 0:
            self.v[0xF] = [0x0]
            difference += 256
        self.v[self.x(self.opcode)] = difference

    def set_vx_to_vx_shr_1(self):
        self.v[0xF] = self.v[self.x(self.opcode)] & 1
        self.v[self.x(self.opcode)] = self.v[self.x(self.opcode)] >> 1

    def set_vx_to_vy_minus_vx(self):
        self.v[0xF] = [0x1]
        difference = self.v[self.y(self.opcode)] - self.v[self.x(self.opcode)]
        if difference < 0:
            self.v[0xF] = [0x0]
            difference += 256
        self.v[self.x(self.opcode)] = difference

    def set_vx_to_vx_shl_1(self):
        self.v[0xF] = (self.v[self.x(self.opcode)] >> 7) & 1
        self.v[self.x(self.opcode)] = self.v[self.x(self.opcode)] << 1

    def skip_if_vx_not_equal_vy(self):
        if not self.v[self.x(self.opcode)] == self.v[self.x(self.opcode)]:
            self.pc += 2

    def set_i_to_nn(self):
        self.i = self.nnn(self.opcode)

    def jump_to_nnn_plus_v0(self):
        self.pc = self.nnn(self.opcode) + self.v[0x0]

    def set_vx_to_random_byte_and_nn(self):
        self.v[self.x(self.opcode)] = int(random() * 256) & self.nn(self.opcode)

    def draw_to_display(self):
        x_cord = self.v[self.x(self.opcode)]
        y_cord = self.v[self.y(self.opcode)]
        height = self.n(self.opcode)
        self.v[0xF] = [0x0]
        y_line = 0

        while y_line < height:
            pixel = self.memory[self.i + y_line]
            x_line = 0
            while x_line < 8:
                if (pixel & (128 >> x_line)) != 0:
                    if (
                        self.display[
                            ((x_cord + x_line) % DISPLAY_WIDTH)
                            + (((y_cord + y_line) % DISPLAY_HEIGHT) * DISPLAY_WIDTH)
                        ] == 1
                    ):
                        self.v[0xF] = [0x1]
                    self.display[
                        ((x_cord + x_line) % DISPLAY_WIDTH)
                        + (((y_cord + y_line) % DISPLAY_HEIGHT) * DISPLAY_WIDTH)
                    ] ^= 1
                x_line += 1
            y_line += 1
        self.draw_flag = True

    def skip_if_key_equals_vx(self):
        if self.keys[self.v[self.x(self.opcode)]] == 1:
            self.pc += 2

    def skip_if_key_not_equal_to_vx(self):
        if not self.keys[self.v[self.x(self.opcode)]] == 1:
            self.pc += 2

    def set_vx_to_delay_timer(self):
        self.v[self.x(self.opcode)] = self.delay_timer

    def store_keypress_in_vx(self):
        key_pressed = False
        index = 0
        while index < 16:
            if self.keys[index] == 1:
                self.v[self.x(self.opcode)] = index
                key_pressed = True
                self.draw_flag = True
            index += 1
        if not key_pressed:
            self.pc -= 2

    def set_delay_timer_to_vx(self):
        self.delay_timer = self.v[self.x(self.opcode)]

    def set_sound_timer_to_vx(self):
        self.sound_timer = self.v[self.x(self.opcode)]

    def set_i_to_i_plus_vx(self):
        self.i += self.v[self.x(self.opcode)]

    def set_i_to_sprite_location_for_vx(self):
        self.i = 5 * self.v[self.x(self.opcode)]

    def store_bcd_in_i(self):
        self.memory[self.i] = self.v[self.x(self.opcode)] // 100
        self.memory[self.i + 1] = (self.v[self.x(self.opcode)] // 10) % 10
        self.memory[self.i + 2] = self.v[self.x(self.opcode)] % 10

    def store_v0_to_vx_in_memory_from_i(self):
        index = 0
        while index <= self.x(self.opcode):
            self.memory[self.i + index] = self.v[index]
            index += 1

    def read_v0_to_vx_from_i(self):
        index = 0
        while index <= self.x(self.opcode):
            self.v[index] = self.memory[self.i + index]
            index += 1

    def least_significant_bits(self, opcode):
        opcode = opcode & 0x000F
        return {
            0x0000: opcode,
            0x000E: opcode
        }.get(opcode, lambda: None)

    def eightxy0_to_eightxye(self, opcode):
        opcode = opcode & 0xF00F
        return {
            0x8000: opcode,
            0x8001: opcode,
            0x8002: opcode,
            0x8003: opcode,
            0x8004: opcode,
            0x8005: opcode,
            0x8006: opcode,
            0x800E: opcode,
        }.get(opcode, lambda: None)

    def ex9e_to_fx65(self, opcode):
        opcode = opcode & 0xF0FF
        return {
            0xE09E: opcode,
            0xE0A1: opcode,
            0xF007: opcode,
            0xF00A: opcode,
            0xF015: opcode,
            0xF018: opcode,
            0xF01E: opcode,
            0xF029: opcode,
            0xF033: opcode,
            0xF055: opcode,
            0xF065: opcode,
        }.get(opcode, lambda: None)

    def execute_opcode(self, decoded_opcode):
        return {
            0x0000: self.clear_screen,
            0x000E: self.return_from_subroutine,
            0x1000: self.jump_to_nnn,
            0x2000: self.call_subroutine_at_nnn,
            0x3000: self.skip_if_vx_equals_nn,
            0x4000: self.skip_if_vx_not_equal_to_nn,
            0x5000: self.skip_if_vx_equals_vy,
            0x6000: self.set_vx_to_nn,
            0x7000: self.set_vx_to_vx_plus_nn,
            0x8000: self.set_vx_to_vy,
            0x8001: self.set_vx_to_vx_or_vy,
            0x8002: self.set_vx_to_vx_and_vy,
            0x8003: self.set_vx_to_vx_xor_vy,
            0x8004: self.set_vx_to_vx_plus_vy,
            0x8005: self.set_vx_to_vx_minus_vy,
            0x8006: self.set_vx_to_vx_shr_1,
            0x8007: self.set_vx_to_vy_minus_vx,
            0x800E: self.set_vx_to_vx_shl_1,
            0x9000: self.skip_if_vx_not_equal_vy,
            0xA000: self.set_i_to_nn,
            0xB000: self.jump_to_nnn_plus_v0,
            0xC000: self.set_vx_to_random_byte_and_nn,
            0xD000: self.draw_to_display,
            0xE09E: self.skip_if_key_equals_vx,
            0xE0A1: self.skip_if_key_not_equal_to_vx,
            0xF007: self.set_vx_to_delay_timer,
            0xF00A: self.store_keypress_in_vx,
            0xF015: self.set_delay_timer_to_vx,
            0xF018: self.set_sound_timer_to_vx,
            0xF01E: self.set_i_to_i_plus_vx,
            0xF029: self.set_i_to_sprite_location_for_vx,
            0xF033: self.store_bcd_in_i,
            0xF055: self.store_v0_to_vx_in_memory_from_i,
            0xF065: self.read_v0_to_vx_from_i,
        }.get(decoded_opcode, lambda: None)()

    def decode_opcode(self, opcode):
        self.first_four_bits_of_opcode = opcode & 0xF000
        return {
            0x0000: self.least_significant_bits(opcode),
            0x8000: self.eightxy0_to_eightxye(opcode),
            0xE000: self.ex9e_to_fx65(opcode),
            0xF000: self.ex9e_to_fx65(opcode),
        }.get(self.first_four_bits_of_opcode, self.first_four_bits_of_opcode)

    def cycle(self):
        self.opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]
        self.pc += 2
        self.decoded_opcode = self.decode_opcode(self.opcode)
        self.execute_opcode(self.decoded_opcode)
        return True
