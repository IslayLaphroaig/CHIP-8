from numpy import fromfile, insert, random, uint8, uint16, zeros
import os

os.chdir("..")


class Chip8:
    def __init__(self):
        self.opcode = uint16(0)
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
            if self.sound_timer == uint8(1):
                print("\a")
            self.sound_timer -= uint8(1)

    def emulate_cycle(self):
        def nnn(opcode):
            return self.opcode & 0x0FFF

        def nn(opcode):
            return self.opcode & 0x00FF

        def n(opcode):
            return self.opcode & 0x000F

        def x(opcode):
            return (self.opcode & 0x0F00) >> uint8(8)

        def y(opcode):
            return (self.opcode & 0x00F0) >> uint8(4)

        self.opcode = (
            self.memory[self.pc] << uint16(8) | self.memory[self.pc + uint16(1)]
        )
        self.pc += uint16(2)

        if self.opcode == 0x00E0:
            self.display.fill(uint8(0))
            self.draw_flag = True

        elif self.opcode == 0x00EE:
            self.stack_pointer -= uint16(1)
            self.pc = self.stack[self.stack_pointer]

        elif self.opcode & 0xF000 == 0x1000:
            self.pc = nnn(self.opcode)

        elif self.opcode & 0xF000 == 0x2000:
            self.stack[self.stack_pointer] = self.pc
            self.stack_pointer += uint16(1)
            self.pc = nnn(self.opcode)

        elif self.opcode & 0xF000 == 0x3000:
            if self.v[x(self.opcode)] == nn(self.opcode):
                self.pc += uint16(2)

        elif self.opcode & 0xF000 == 0x4000:
            if not self.v[x(self.opcode)] == nn(self.opcode):
                self.pc += uint16(2)

        elif self.opcode & 0xF000 == 0x5000:
            if not self.v[x(self.opcode)] == nn(self.opcode):
                self.pc += uint16(2)

        elif self.opcode & 0xF000 == 0x6000:
            self.v[x(self.opcode)] = nn(self.opcode)

        elif self.opcode & 0xF000 == 0x7000:
            self.v[x(self.opcode)] += nn(self.opcode)

        elif self.opcode & 0xF00F == 0x8000:
            self.v[x(self.opcode)] = self.v[y(self.opcode)]

        elif self.opcode & 0xF00F == 0x8001:
            self.v[x(self.opcode)] = self.v[x(self.opcode)] | self.v[y(self.opcode)]

        elif self.opcode & 0xF00F == 0x8002:
            self.v[x(self.opcode)] = self.v[x(self.opcode)] & self.v[y(self.opcode)]

        elif self.opcode & 0xF00F == 0x8003:
            self.v[x(self.opcode)] = self.v[x(self.opcode)] ^ self.v[y(self.opcode)]

        elif self.opcode & 0xF00F == 0x8004:
            self.v[0xF] = uint8(0)
            total = uint16(self.v[x(self.opcode)]) + uint16(self.v[y(self.opcode)])
            if total > uint16(255):
                self.v[0xF] = uint8(1)
                total -= uint16(256)
            self.v[x(self.opcode)] = uint16(total)

        elif self.opcode & 0xF00F == 0x8005:
            self.v[0xF] = uint8(1)
            difference = uint16(self.v[x(self.opcode)]) - uint16(self.v[y(self.opcode)])
            if difference < uint8(0):
                self.v[0xF] = uint8(0)
                difference += uint8(256)
            self.v[x(self.opcode)] = uint16(difference)

        elif self.opcode & 0xF00F == 0x8006:
            self.v[0xF] = self.v[x(self.opcode)] & uint8(1)
            self.v[x(self.opcode)] = self.v[x(self.opcode)] >> uint8(1)

        elif self.opcode & 0xF00F == 0x8007:
            self.v[0xF] = uint8(1)
            difference = uint16(self.v[y(self.opcode)]) - uint16(self.v[x(self.opcode)])
            if difference < uint8(0):
                self.v[0xF] = uint8(0)
                difference += uint8(256)
            self.v[x(self.opcode)] = uint16(difference)

        elif self.opcode & 0xF00F == 0x800E:
            self.v[0xF] = (self.v[x(self.opcode)] >> uint8(7)) & uint8(1)
            self.v[x(self.opcode)] = self.v[x(self.opcode)] << uint8(1)

        elif self.opcode & 0xF000 == 0x9000:
            if not self.v[x(self.opcode)] == self.v[x(self.opcode)]:
                self.pc += 2

        elif self.opcode & 0xF000 == 0xA000:
            self.i = nnn(self.opcode)

        elif self.opcode & 0xF000 == 0xB000:
            self.pc = nnn(self.opcode) + self.v[0x0]

        elif self.opcode & 0xF000 == 0xC000:
            random.randint(0, 255, dtype=uint8) & nn(self.opcode)

        elif self.opcode & 0xF000 == 0xD000:
            x = self.v[x(self.opcode)]
            y = self.v[y(self.opcode)]
            height = n(self.opcode)
            self.v[0xF] = uint8(0)
            y_line = uint16(0)

            while y_line < height:
                pixel = self.memory[self.i + y_line]
                x_line = uint16(0)
                while x_line < uint16(8):
                    if (pixel & (uint8(0x80) >> x_line)) != uint8(0):
                        if self.display[
                            x + x_line + ((y + y_line) * uint8(64))
                        ] == uint8(1):
                            self.v[0xF] = uint8(0x1)
                        self.display[x + x_line + ((y + y_line) * uint8(64))] ^= uint8(1)
                    x_line += uint16(1)
                y_line += uint16(1)
            self.draw_flag = True

        elif self.opcode & 0xF0FF == 0xE09E:
            if self.keys[self.v[x(self.opcode)]] == uint8(1):
                self.pc += uint16(2)

        elif self.opcode & 0xF0FF == 0xE0A1:
            if not self.keys[self.v[x(self.opcode)]] == uint8(1):
                self.pc += uint16(2)

        elif self.opcode & 0xF0FF == 0xF007:
            self.v[x(self.opcode)] = self.delay_timer

        elif self.opcode & 0xF0FF == 0xF00A:
            key_pressed = False
            index = uint8(0)
            while index < uint8(16):
                if self.keys[index] == uint8(1):
                    self.v[x(self.opcode)] = index
                    key_pressed = True
            if not key_pressed:
                self.pc += uint16(2)

        elif self.opcode & 0xF0FF == 0xF015:
            self.delay_timer = self.v[x(self.opcode)]

        elif self.opcode & 0xF0FF == 0xF018:
            self.sound_timer = self.v[x(self.opcode)]

        elif self.opcode & 0xF0FF == 0xF01E:
            self.i += self.v[x(self.opcode)]

        elif self.opcode & 0xF0FF == 0xF029:
            self.i = uint16(5) * self.v[x(self.opcode)]

        elif self.opcode & 0xF0FF == 0xF033:
            self.memory[self.i] = self.v[x(self.opcode)] / uint8(100)
            self.memory[self.i + uint16(1)] = (
                self.v[x(self.opcode)] / uint8(10)
            ) % uint8(10)
            self.memory[self.i + uint16(2)] = self.v[x(self.opcode)] % uint8(10)

        elif self.opcode & 0xF0FF == 0xF055:
            index = uint16(0)
            while index <= x(self.opcode):
                self.memory[self.i + index] = self.v[index]
                index += uint16(1)

        elif self.opcode & 0xF0FF == 0xF065:
            index = uint16(0)
            while index <= x(self.opcode):
                self.v[index] = self.memory[self.i + index]
                index += uint16(1)

        else:
            print("Invalid Opcode", self.opcode)
            return False

        return True
