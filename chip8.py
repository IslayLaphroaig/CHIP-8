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
        self.stack = zeros(16, dtype=uint8)
        self.stack_pointer = uint16(0)
        self.delay_timer = uint8(0)
        self.sound_timer = uint8(0)
        self.keys = zeros(16, dtype=uint8)
        self.display = zeros(64 * 32, dtype=uint8)
        self.memory = insert(self.memory, 0x50, self.font_set, axis=0)

    def load_rom(self, rom):
        data = fromfile(rom, dtype=uint8)
        self.memory = insert(self.memory, 0x200, data, axis=0)

    def emulate_cycle(self):
        NNN = lambda opcode : bitwise_and(self.opcode, 0XFFF) # Address
        NN  = lambda opcode : bitwise_and(self.opcode, 0XFF) # 8-bit constant
        N   = lambda opcode : bitwise_and(self.opcode, 0xF) # 4-bit constant
        X   = lambda opcode : bitwise_and(right_shift(self.opcode, uint16(8)), 0xF) # X Register
        Y   = lambda opcode : bitwise_and(right_shift(self.opcode, uint16(4)), 0xF) # Y Register

        # fetch opcode
        self.opcode = bitwise_or(left_shift(self.memory[self.PC], uint16(8)), self.memory[self.PC + 1])

        #decode opcode
        if(bitwise_and(self.opcode, 0xF000)) == 0x0000:
            print("0x0000")

        elif(self.opcode == 0x00E0):
            print("0x00E0")

        elif(self.opcode == 0x00EE):
            print("0x00EE")

        elif(bitwise_and(self.opcode, 0xF000)) == 0x1000:
            print("0x1000")    

        elif(bitwise_and(self.opcode, 0xF000)) == 0x2000:
            print("0x2000")

        elif(bitwise_and(self.opcode, 0xF000)) == 0x3000:
            print("0x3000")

        elif(bitwise_and(self.opcode, 0xF000)) == 0x4000:
            print("0x4000")

        elif(bitwise_and(self.opcode, 0xF000)) == 0x5000:
            print("0x5000")

        elif(bitwise_and(self.opcode, 0xF000)) == 0x6000:
            print("0x6000")
            self.V[X(self.opcode)] = NN(self.opcode)
            self.PC += 2

        elif(bitwise_and(self.opcode, 0xF000)) == 0x7000:
            print("0x7000")

        elif(bitwise_and(self.opcode, 0xF000)) == 0x8000:
            print("0x8000")

        elif(bitwise_and(self.opcode, 0xF000)) == 0x8001:
            print("0x8001")

        elif(bitwise_and(self.opcode, 0xF000)) == 0x8002:
            print("0x8002")

        elif(bitwise_and(self.opcode, 0xF000)) == 0x8003:
            print("0x8003")

        elif(bitwise_and(self.opcode, 0xF000)) == 0x8004:
            print("0x8004")

        elif(bitwise_and(self.opcode, 0xF000)) == 0x8005:
            print("0x8005")

        elif(bitwise_and(self.opcode, 0xF000)) == 0x8006:
            print("0x8006")

        elif(bitwise_and(self.opcode, 0xF000)) == 0x8007:
            print("0x8007")

        elif(bitwise_and(self.opcode, 0xF000)) == 0x8008:
            print("0x8008")

        elif(bitwise_and(self.opcode, 0xF000)) == 0x9000:
            print("0x9000")

        elif(bitwise_and(self.opcode, 0xF000)) == 0xA000:
            print("0xA000")
            self.I = NNN(self.opcode)
            self.PC += 2

        elif(bitwise_and(self.opcode, 0xF000)) == 0xB000:
            print("0xB000")

        elif(bitwise_and(self.opcode, 0xF000)) == 0xC000:
            print("0xC000")

        elif(bitwise_and(self.opcode, 0xF000)) == 0xD000:
            print("0xD000")
            x = uint16(self.V[X(self.opcode)])
            y = uint16(self.V[Y(self.opcode)])
            height = uint16(N(self.opcode))
            pixel = uint16(0)
            self.V[0xF] = 0
            yline = uint16(0)

            while yline < height:
                pixel = self.memory[self.I + yline]
                xline = uint16(0)
                while xline < uint16(8):
                    if(right_shift(pixel, xline)) != 0:
                        if(self.display[x + xline + ((y + yline) * 64)] == 0):
                            self.V[0xF] = 1
                        elif self.display[x + xline + ((y + yline) * 64)] == 1:
                            self.V[0xF] = 2

            self.PC +=2

        elif(bitwise_and(self.opcode, 0xF000)) == 0xE09E:
            print("0xE09E")

        elif(bitwise_and(self.opcode, 0xF000)) == 0xE0A1:
            print("0xE0A1")

        elif(bitwise_and(self.opcode, 0xF000)) == 0xF007:
            print("0xF007")

        elif(bitwise_and(self.opcode, 0xF000)) == 0xF00A:
            print("0xF00A")

        elif(bitwise_and(self.opcode, 0xF000)) == 0xF015:
            print("0xF015")

        elif(bitwise_and(self.opcode, 0xF000)) == 0xF018:
            print("0xF018")

        elif(bitwise_and(self.opcode, 0xF000)) == 0xF01E:
            print("0xF01E")

        elif(bitwise_and(self.opcode, 0xF000)) == 0xF029:
            print("0xF029")

        elif(bitwise_and(self.opcode, 0xF000)) == 0xF033:
            print("0xF033")

        elif(bitwise_and(self.opcode, 0xF000)) == 0xF055:
            print("0xF055")

        elif(bitwise_and(self.opcode, 0xF000)) == 0xF065:
            print("0xF065")

        else:
            print("Invalid Opcode")
            return False
        
        return True