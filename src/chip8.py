from numpy import fromfile, insert, int16, random, uint8, uint16, zeros


class Chip8:
    def __init__(self):
        self.opcode = uint16(0)
        self.bitwise_opcode = uint16(0)
        self.memory = zeros(4096, dtype=uint8)
        self.v = zeros(16, dtype=uint8)
        self.i = uint16(0)
        self.pc = uint16(0x200)
        self.stack = zeros(16, dtype=uint16)
        self.stack_pointer = uint16(0)
        self.delay_timer = uint8(0)
        self.sound_timer = uint8(0)
        self.keys = zeros(16, dtype=uint8)
        self.display = zeros(64 * 32, dtype=uint8)
        self.draw_flag = False
        self.memory = insert(
            self.memory, 0x0, fromfile("font_set", dtype=uint8), axis=0
        )

    def load_rom(self, rom):
        data = fromfile(rom, dtype=uint8)
        self.memory = insert(self.memory, 0x200, data, axis=0)

    def update_timers(self):
        if self.delay_timer > uint8(0):
            self.delay_timer -= uint8(1)

        if self.sound_timer > uint8(0):
            self.sound_timer -= uint8(1)

    def nnn(self, opcode):
        return opcode & 0x0FFF

    def nn(self, opcode):
        return opcode & 0x00FF

    def n(self, opcode):
        return opcode & 0x000F

    def x(self, opcode):
        return (opcode & 0x0F00) >> uint8(8)

    def y(self, opcode):
        return (opcode & 0x00F0) >> uint8(4)

    def clear_screen(self):
        self.display.fill(uint8(0))
        self.draw_flag = True

    def return_from_subroutine(self):
        self.stack_pointer -= uint16(1)
        self.pc = self.stack[self.stack_pointer]

    def jump_to_nnn(self):
        self.pc = self.nnn(self.opcode)

    def call_subroutine_at_nnn(self):
        self.stack[self.stack_pointer] = self.pc
        self.stack_pointer += uint16(1)
        self.pc = self.nnn(self.opcode)

    def skip_if_vx_equals_nn(self):
        if self.v[self.x(self.opcode)] == self.nn(self.opcode):
            self.pc += uint16(2)

    def skip_if_vx_not_equal_to_nn(self):
        if not self.v[self.x(self.opcode)] == self.nn(self.opcode):
            self.pc += uint16(2)

    def skip_if_vx_equals_vy(self):
        if not self.v[self.x(self.opcode)] == self.nn(self.opcode):
            self.pc += uint16(2)

    def set_vx_to_nn(self):
        self.v[self.x(self.opcode)] = self.nn(self.opcode)

    def set_vx_to_vx_plus_nn(self):
        self.v[self.x(self.opcode)] += self.nn(self.opcode)

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
        self.v[0xF] = uint8(0)
        total = uint16(self.v[self.x(self.opcode)]) + uint16(
            self.v[self.y(self.opcode)]
        )
        if total > uint16(255):
            self.v[0xF] = uint8(1)
            total -= uint16(256)
        self.v[self.x(self.opcode)] = uint16(total)

    def set_vx_to_vx_minus_vy(self):
        self.v[0xF] = uint8(1)
        difference = int16(self.v[self.x(self.opcode)]) - int16(
            self.v[self.y(self.opcode)]
        )
        if difference < uint16(0):
            self.v[0xF] = uint8(0)
            difference += uint16(256)
        self.v[self.x(self.opcode)] = uint16(difference)

    def set_vx_to_vx_shr_1(self):
        self.v[0xF] = self.v[self.x(self.opcode)] & uint8(1)
        self.v[self.x(self.opcode)] = self.v[self.x(self.opcode)] >> uint8(1)

    def set_vx_to_vy_minus_vx(self):
        self.v[0xF] = uint8(1)
        difference = int16(self.v[self.y(self.opcode)]) - int16(
            self.v[self.x(self.opcode)]
        )
        if difference < uint8(0):
            self.v[0xF] = uint8(0)
            difference += uint8(256)
        self.v[self.x(self.opcode)] = uint16(difference)

    def set_vx_to_vx_shl_1(self):
        self.v[0xF] = (self.v[self.x(self.opcode)] >> uint8(7)) & uint8(1)
        self.v[self.x(self.opcode)] = self.v[self.x(self.opcode)] << uint8(1)

    def skip_if_vx_not_equal_vy(self):
        if not self.v[self.x(self.opcode)] == self.v[self.x(self.opcode)]:
            self.pc += 2

    def set_i_to_nn(self):
        self.i = self.nnn(self.opcode)

    def jump_to_nnn_plus_v0(self):
        self.pc = self.nnn(self.opcode) + self.v[0x0]

    def set_vx_to_random_byte_and_nn(self):
        random.randint(0, 255, dtype=uint8) & self.nn(self.opcode)

    def draw_to_display(self):
        x_cord = self.v[self.x(self.opcode)]
        y_cord = self.v[self.y(self.opcode)]
        height = self.n(self.opcode)
        self.v[0xF] = uint8(0)
        y_line = uint16(0)

        while y_line < height:
            pixel = self.memory[self.i + y_line]
            x_line = uint16(0)
            while x_line < uint16(8):
                if (pixel & (uint8(0x80) >> x_line)) != uint8(0):
                    if self.display[
                        x_cord + x_line + ((y_cord + y_line) * uint8(64))
                    ] == uint8(1):
                        self.v[0xF] = uint8(0x1)
                    self.display[
                        x_cord + x_line + ((y_cord + y_line) * uint8(64))
                    ] ^= uint8(1)
                x_line += uint16(1)
            y_line += uint16(1)
        self.draw_flag = True

    def skip_if_key_equals_vx(self):
        if self.keys[self.v[self.x(self.opcode)]] == uint8(1):
            self.pc += uint16(2)

    def skip_if_key_not_equal_to_vx(self):
        if not self.keys[self.v[self.x(self.opcode)]] == uint8(1):
            self.pc += uint16(2)

    def set_vx_to_delay_timer(self):
        self.v[self.x(self.opcode)] = self.delay_timer

    def store_keypress_in_vx(self):
        key_pressed = False
        index = uint8(0)
        while index < uint8(16):
            if self.keys[index] == uint8(1):
                self.v[self.x(self.opcode)] = index
                key_pressed = True
        if not key_pressed:
            self.pc += uint16(2)

    def set_delay_timer_to_vx(self):
        self.delay_timer = self.v[self.x(self.opcode)]

    def set_sound_timer_to_vx(self):
        self.sound_timer = self.v[self.x(self.opcode)]

    def set_i_to_i_plus_vx(self):
        self.i += self.v[self.x(self.opcode)]

    def set_i_to_sprite_location_for_vx(self):
        self.i = uint16(5) * self.v[self.x(self.opcode)]

    def store_bcd_in_i(self):
        self.memory[self.i] = self.v[self.x(self.opcode)] / uint8(100)
        self.memory[self.i + uint16(1)] = (
            self.v[self.x(self.opcode)] / uint8(10)
        ) % uint8(10)
        self.memory[self.i + uint16(2)] = self.v[self.x(self.opcode)] % uint8(10)

    def store_v0_to_vx_in_memory_from_i(self):
        index = uint16(0)
        while index <= self.x(self.opcode):
            self.memory[self.i + index] = self.v[index]
            index += uint16(1)

    def read_v0_to_vx_from_i(self):
        index = uint16(0)
        while index <= self.x(self.opcode):
            self.v[index] = self.memory[self.i + index]
            index += uint16(1)

    def bitwise(self, opcode):
        if opcode == 0x00E0:
            return 0x00E0
        elif opcode == 0x00EE:
            return 0x00EE
        elif opcode & 0xF000 == 0x1000:
            return 0x1000
        elif opcode & 0xF000 == 0x2000:
            return 0x2000
        elif opcode & 0xF000 == 0x3000:
            return 0x3000
        elif opcode & 0xF000 == 0x4000:
            return 0x4000
        elif opcode & 0xF000 == 0x5000:
            return 0x5000
        elif opcode & 0xF000 == 0x6000:
            return 0x6000
        elif opcode & 0xF000 == 0x7000:
            return 0x7000
        elif opcode & 0xF00F == 0x8000:
            return 0x8000
        elif opcode & 0xF00F == 0x8001:
            return 0x8001
        elif opcode & 0xF00F == 0x8002:
            return 0x8002
        elif opcode & 0xF00F == 0x8003:
            return 0x8003
        elif opcode & 0xF00F == 0x8004:
            return 0x8004
        elif opcode & 0xF00F == 0x8005:
            return 0x8005
        elif opcode & 0xF00F == 0x8006:
            return 0x8006
        elif opcode & 0xF00F == 0x8007:
            return 0x8007
        elif opcode & 0xF00F == 0x800E:
            return 0x800E
        elif opcode & 0xF000 == 0x9000:
            return 0x9000
        elif opcode & 0xF000 == 0xA000:
            return 0xA000
        elif opcode & 0xF000 == 0xB000:
            return 0xB000
        elif opcode & 0xF000 == 0xC000:
            return 0xC000
        elif opcode & 0xF000 == 0xD000:
            return 0xD000
        elif opcode & 0xF0FF == 0xE09E:
            return 0xE09E
        elif opcode & 0xF0FF == 0xE0A1:
            return 0xE0A1
        elif opcode & 0xF0FF == 0xF007:
            return 0xF007
        elif opcode & 0xF0FF == 0xF00A:
            return 0xF00A
        elif opcode & 0xF0FF == 0xF015:
            return 0xF015
        elif opcode & 0xF0FF == 0xF018:
            return 0xF018
        elif opcode & 0xF0FF == 0xF01E:
            return 0xF01E
        elif opcode & 0xF0FF == 0xF029:
            return 0xF029
        elif opcode & 0xF0FF == 0xF033:
            return 0xF033
        elif opcode & 0xF0FF == 0xF055:
            return 0xF055
        elif opcode & 0xF0FF == 0xF065:
            return 0xF065
        else:
            return False

    def opcode_dictionary(self, bitwise_opcode):
        return {
            0x00E0: self.clear_screen,
            0x00EE: self.return_from_subroutine,
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
        }.get(bitwise_opcode, lambda: None)()

    def cycle(self):
        self.opcode = (
            self.memory[self.pc] << uint16(8) | self.memory[self.pc + uint16(1)]
        )
        self.pc += uint16(2)

        self.bitwise_opcode = self.bitwise(self.opcode)
        self.opcode_dictionary(self.bitwise_opcode)

        return True
