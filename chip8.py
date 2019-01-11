from numpy import *

class Chip8:

    set_printoptions(threshold=nan) # for debugging
    set_printoptions(formatter={'int':lambda x:hex(int(x))}) # for debugging

    font_set = array([
            0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
            0x20, 0x60, 0x20, 0x20, 0x70, # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
            0x90, 0x90, 0xF0, 0x10, 0x10, # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
            0xF0, 0x10, 0x20, 0x40, 0x40, # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90, # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
            0xF0, 0x80, 0x80, 0x80, 0xF0, # C
            0xE0, 0x90, 0x90, 0x90, 0xE0, # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
            0xF0, 0x80, 0xF0, 0x80, 0x80  # F
            ], dtype=uint8)

    def __init__(self):
        self.opcode = uint16(0)
        self.memory = zeros(4096, dtype=uint8)
        self.V = zeros(16, dtype=uint8)
        self.I = uint16(0)
        self.PC = uint16(0x200)
        self.stack = zeros(16, dtype=uint16)
        self.stack_pointer = uint16(0)
        self.delay_timer = uint8(0)
        self.sound_timer = uint8(0)
        self.keys = zeros(16, dtype=uint8)
        self.display = zeros(64 * 32, dtype=uint8)
        self.memory = insert(self.memory, 0x50, self.font_set, axis=0)
        self.draw_flag = False

    def load_rom(self, rom):
        data = fromfile(rom, dtype=uint8)
        self.memory = insert(self.memory, 0x200, data, axis=0)

    def emulate_cycle(self):
        NNN = lambda opcode : bitwise_and(self.opcode, 0XFFF) # A 12-bit value, the lowest 12 bits of the instruction
        KK  = lambda opcode : bitwise_and(self.opcode, 0XFF) # An 8-bit value, the lowest 8 bits of the instruction
        N   = lambda opcode : bitwise_and(self.opcode, 0xF) # A 4-bit value, the lowest 4 bits of the instruction
        X   = lambda opcode : bitwise_and(right_shift(self.opcode, uint16(8)), 0xF) # A 4-bit value, the lower 4 bits of the high byte of the instruction
        Y   = lambda opcode : bitwise_and(right_shift(self.opcode, uint16(4)), 0xF) # A 4-bit value, the upper 4 bits of the low byte of the instruction

        # fetch opcode
        self.opcode = bitwise_or(left_shift(self.memory[self.PC], uint16(8)), self.memory[self.PC + uint16(1)])

        #decode opcode
        if(self.opcode == 0x00E0):
            print("0x00E0")
            zeros(self.display)

        elif(self.opcode == 0x00EE):
            print("0x00EE")
            self.PC = self.stack[0]
            self.stack_pointer -= uint16(1)
            self.PC += 2

        elif(bitwise_and(self.opcode, 0xF000)) == 0x1000:
            print("0x1000")
            self.PC = NNN(self.opcode)

        elif(bitwise_and(self.opcode, 0xF000)) == 0x2000:
            print("0x2000")
            self.stack[self.stack_pointer] = self.PC
            self.stack_pointer += uint16(1)
            self.PC = uint16(NNN(self.opcode))

        elif(bitwise_and(self.opcode, 0xF000)) == 0x3000:
            print("0x3000")
            if self.V[X(self.opcode)] == KK(self.opcode):
                self.PC += uint16(2)
            self.PC += uint16(2)

        elif(bitwise_and(self.opcode, 0xF000)) == 0x4000:
            print("0x4000")
            if(self.V[X(self.opcode)]) == KK(self.opcode):
                self.PC += uint16(2)
            self.PC += uint16(2)

        elif(bitwise_and(self.opcode, 0xF000)) == 0x5000:
            print("0x5000")
            if(self.V[X(self.opcode)]) != KK(self.opcode):
                self.PC += uint16(2)
            self.PC += uint16(2)

        elif(bitwise_and(self.opcode, 0xF000)) == 0x6000:
            print("0x6000")
            self.V[X(self.opcode)] = KK(self.opcode)
            self.PC += uint16(2)

        elif(bitwise_and(self.opcode, 0xF000)) == 0x7000:
            print("0x7000")
            self.V[X(self.opcode)] = self.V[Y(self.opcode)]
            self.PC += uint16(2)

        elif(bitwise_and(self.opcode, 0xF00F)) == 0x8000:
            print("0x8000")
            self.V[X(self.opcode)] = self.V[Y(self.opcode)]
            self.PC += uint16(2)

        elif(bitwise_and(self.opcode, 0xF00F)) == 0x8001:
            print("0x8001")
            self.V[X(self.opcode)] = bitwise_or(self.V[X(self.opcode)], self.V[Y(self.opcode)])
            self.PC += uint16(2)

        elif(bitwise_and(self.opcode, 0xF00F)) == 0x8002:
            print("0x8002")
            self.V[X(self.opcode)] = bitwise_and(self.V[X(self.opcode)], self.V[Y(self.opcode)])
            self.PC += uint16(2)

        elif(bitwise_and(self.opcode, 0xF00F)) == 0x8003:
            print("0x8003")
            self.V[X(self.opcode)] = bitwise_xor(self.V[X(self.opcode)], self.V[Y(self.opcode)])
            self.PC += uint16(2)

        elif(bitwise_and(self.opcode, 0xF00F)) == 0x8004:
            print("0x8004")
            if (self.V[Y(self.opcode)]) > (0xFF - self.V[X(self.opcode)]):
                self.V[0xF] = 1
            else:
                self.V[0xF] = 0
            self.V[X(self.opcode)] += self.V[Y(self.opcode)]
            self.PC += uint16(2)

        elif(bitwise_and(self.opcode, 0xF00F)) == 0x8005:
            print("0x8005")
            if self.V[X(self.opcode)] > self.V[Y(self.opcode)]:
                self.V[0xF] = uint8(1)
            else:
                self.V[0xF] = uint8(0)
            self.V[X(self.opcode)] -= self.V[Y(self.opcode)]
            self.PC += uint16(2)

        elif(bitwise_and(self.opcode, 0xF00F)) == 0x8006:
            print("0x8006")

        elif(bitwise_and(self.opcode, 0xF00F)) == 0x8007:
            print("0x8007")

        elif(bitwise_and(self.opcode, 0xF00F)) == 0x8008:
            print("0x8008")

        elif(bitwise_and(self.opcode, 0xF000)) == 0x9000:
            print("0x9000")

        elif(bitwise_and(self.opcode, 0xF000)) == 0xA000:
            print("0xA000")
            self.I = NNN(self.opcode)
            self.PC += uint16(2)

        elif(bitwise_and(self.opcode, 0xF000)) == 0xB000:
            print("0xB000")

        elif(bitwise_and(self.opcode, 0xF000)) == 0xC000:
            print("0xC000")
            bitwise_and(random.randint(0, 255, dtype=uint8), KK(self.opcode))
            self.PC += uint16(2)

        elif(bitwise_and(self.opcode, 0xF000)) == 0xD000:
            print("0xD000")
            x = uint16(self.V[right_shift(bitwise_and(self.opcode, 0x0F00), uint8(8))])
            y = uint16(self.V[right_shift(bitwise_and(self.opcode, 0x00F0), uint8(4))])
            height = uint16(bitwise_and(self.opcode, 0x000F))
            pixel = uint16(0)
            yline = uint16(0)
            self.V[0xF] = uint8(0)

            while yline < height:
                pixel = uint16(self.memory[self.I + yline])
                xline = uint16(0)
                while xline < uint16(8):
                    if(bitwise_and(pixel, right_shift(int8(0x80), xline)) != uint8(0)):
                        if(self.display[(x + xline + ((y + yline) * uint8(64)))] == uint8(1)):
                            self.V[0xF] = uint8(1)
                            self.display = bitwise_xor(self.display[x + xline + ((y + yline) * uint8(64))], uint8(1))
                    xline += uint16(1)
                yline += uint16(1)
            
            self.draw_flag = True
            self.PC += uint16(2)

        elif(bitwise_and(self.opcode, 0xF0FF)) == 0xE09E:
            print("0xE09E")

        elif(bitwise_and(self.opcode, 0xF0FF)) == 0xE0A1:
            print("0xE0A1")
            if not self.keys[self.V[X(self.opcode)]]:
                self.PC += uint16(2)
            self.PC += uint16(2)

        elif(bitwise_and(self.opcode, 0xF0FF)) == 0xF007:
            print("0xF007")
            self.V[X(self.opcode)] += KK(self.opcode)
            self.PC += uint16(2)

        elif(bitwise_and(self.opcode, 0xF0FF)) == 0xF00A:
            print("0xF00A")

        elif(bitwise_and(self.opcode, 0xF0FF)) == 0xF015:
            print("0xF015")
            self.delay_timer = self.V[X(self.opcode)]
            self.PC += uint16(2)

        elif(bitwise_and(self.opcode, 0xF0FF)) == 0xF018:
            print("0xF018")
            self.sound_timer = self.V[X(self.opcode)]
            self.PC += uint16(2)

        elif(bitwise_and(self.opcode, 0xF0FF)) == 0xF01E:
            print("0xF01E")
            self.I = self.V[X(self.opcode)]
            self.PC += uint16(2)

        elif(bitwise_and(self.opcode, 0xF0FF)) == 0xF029:
            print("0xF029")
            self.I = uint16(5) * self.V[X(self.opcode)]
            self.PC += uint16(2)

        elif(bitwise_and(self.opcode, 0xF0FF)) == 0xF033:
            print("0xF033")
            self.memory[self.I] = self.V[X(self.opcode)] / uint16(100)
            self.memory[self.I + 1] = self.V[X(self.opcode)] / uint16(10) % 10
            self.memory[self.I + 2] = self.V[X(self.opcode)] % uint16(100) % 10
            self.PC += uint16(2)

        elif(bitwise_and(self.opcode, 0xF0FF)) == 0xF055:
            print("0xF055")
            self.memory = insert(self.memory,
                                 self.memory[self.I:self.I + X(self.opcode) + 1],
                                 self.V[X(self.opcode) + 1],
                                 axis=0)
            self.PC += 2

        elif(bitwise_and(self.opcode, 0xF0FF)) == 0xF065:
            print("0xF065")
            self.V = insert(self.V,
                            self.V[X(self.opcode) + 1],
                            self.memory[self.I:self.I + X(self.opcode) + 1],
                            axis=0)
            self.PC += 2

        else:
            print("Invalid Opcode", self.opcode)
            return False
        
        return True