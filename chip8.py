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
        self.memory = insert(self.memory, 0x0, self.font_set, axis=0)
        self.draw_flag = False

    def load_rom(self, rom):
        data = fromfile(rom, dtype=uint8)
        self.memory = insert(self.memory, 0x200, data, axis=0)        

    def update_timers(self):
        if self.delay_timer > uint8(0):
            self.delay_timer -= uint8(1)
            
        if self.sound_timer > 0:
            if self.sound_timer == 1:
                print("\a") #simple alarm sound
            self.sound_timer -= 1

    def emulate_cycle(self):
        NNN = lambda opcode : self.opcode & 0X0FFF # A 12-bit value, the lowest 12 bits of the instruction
        NN  = lambda opcode : self.opcode & 0X00FF # An 8-bit value, the lowest 8 bits of the instruction
        N   = lambda opcode : self.opcode & 0x000F # A 4-bit value, the lowest 4 bits of the instruction
        X   = lambda opcode : (self.opcode & 0x0F00) >> uint8(8) # A 4-bit value, the lower 4 bits of the high byte of the instruction
        Y   = lambda opcode : (self.opcode & 0x00F0) >> uint8(4) # A 4-bit value, the upper 4 bits of the low byte of the instruction

        # fetch opcode
        self.opcode = self.memory[self.PC] << uint16(8) | self.memory[self.PC + uint16(1)]
        self.PC += uint16(2)

        #decode opcode
        if self.opcode == 0x00E0:
            print("0x00E0")
            self.display.fill(uint8(0))
            self.draw_flag = True

        elif self.opcode == 0x00EE:
            print("0x00EE")
            self.stack_pointer -= uint16(1)
            self.PC = self.stack[self.stack_pointer]

        elif self.opcode & 0xF000 == 0x1000:
            print("0x1000")
            self.PC = NNN(self.opcode)

        elif self.opcode & 0xF000 == 0x2000:
            print("0x2000")
            self.stack[self.stack_pointer] = self.PC
            self.stack_pointer += uint16(1)
            self.PC = NNN(self.opcode)

        elif self.opcode & 0xF000 == 0x3000:
            print("0x3000")
            if self.V[X(self.opcode)] == NN(self.opcode):
                self.PC += uint16(2)

        elif self.opcode & 0xF000 == 0x4000:
            print("0x4000")
            if not self.V[X(self.opcode)] == NN(self.opcode):
                self.PC += uint16(2)

        elif self.opcode & 0xF000 == 0x5000:
            print("0x5000")
            if not self.V[X(self.opcode)] == NN(self.opcode):
                self.PC += uint16(2)

        elif self.opcode & 0xF000 == 0x6000:
            print("0x6000")
            self.V[X(self.opcode)] = NN(self.opcode)

        elif self.opcode & 0xF000 == 0x7000:
            print("0x7000")
            self.V[X(self.opcode)] += NN(self.opcode)

        elif self.opcode & 0xF00F == 0x8000:
            print("0x8000")
            self.V[X(self.opcode)] = self.V[Y(self.opcode)]

        elif self.opcode & 0xF00F == 0x8001:
            print("0x8001")
            self.V[X(self.opcode)] = self.V[X(self.opcode)] | self.V[Y(self.opcode)]

        elif self.opcode & 0xF00F == 0x8002:
            print("0x8002")
            self.V[X(self.opcode)] = self.V[X(self.opcode)] & self.V[Y(self.opcode)]

        elif self.opcode & 0xF00F == 0x8003:
            print("0x8003")
            self.V[X(self.opcode)] = self.V[X(self.opcode)] ^ self.V[Y(self.opcode)]

        elif self.opcode & 0xF00F == 0x8004:
            print("0x8004")
            self.V[0xF] = uint8(0)
            total = uint16(self.V[X(self.opcode)]) + uint16(self.V[Y(self.opcode)])
            if total > uint16(255):
                self.V[0xF] = uint8(1)
                total -= uint16(256)
            self.V[X(self.opcode)] = uint16(total)

        elif self.opcode & 0xF00F == 0x8005:
            print("0x8005")
            self.V[0xF] = uint8(1)
            difference = int16(self.V[X(self.opcode)]) - int16(self.V[Y(self.opcode)])
            if difference < uint8(0):
                self.V[0xF] = uint8(0)
                difference += uint8(256)
            self.V[X(self.opcode)] = uint16(difference)

        elif self.opcode & 0xF00F == 0x8006:
            print("0x8006")
            self.V[0xF] = self.V[X(self.opcode)] & uint8(1)
            self.V[X(self.opcode)] = self.V[X(self.opcode)] >> uint8(1)

        elif self.opcode & 0xF00F == 0x8007:
            print("0x8007")
            self.V[0xf] = uint8(1)
            difference = int16(self.V[Y(self.opcode)]) - int16(self.V[X(self.opcode)])
            if difference < uint8(0):
                self.V[0xF] = uint8(0)
                difference += uint8(256)
            self.V[X(self.opcode)] = uint16(difference)

        elif self.opcode & 0xF00F == 0x800E:
            print("0x800E")
            self.V[0xF] = (self.V[X(self.opcode)] >> uint8(7)) & uint8(1)
            self.V[X(self.opcode)] = self.V[X(self.opcode)] << uint8(1)

        elif self.opcode & 0xF000 == 0x9000:
            print("0x9000")

        elif self.opcode & 0xF000 == 0xA000:
            print("0xA000")
            self.I = NNN(self.opcode)

        elif self.opcode & 0xF000 == 0xB000:
            print("0xB000")

        elif self.opcode & 0xF000 == 0xC000:
            print("0xC000")
            random.randint(0, 255, dtype=uint8) & NN(self.opcode)
            
        elif self.opcode & 0xF000 == 0xD000:
            x = self.V[X(self.opcode)]
            y = self.V[Y(self.opcode)]
            height = N(self.opcode)
            self.V[0xF] = uint8(0)
            yline = uint16(0)
            
            while yline < height:
                pixel = self.memory[self.I + yline]
                xline = uint16(0)
                while xline < uint16(8):
                    if((pixel & (uint8(0x80) >> xline)) != uint8(0)):
                        if(self.display[x + xline + ((y + yline) * uint8(64))] == uint8(1)):
                            self.V[0xF] = uint8(0x1)
                        self.display[x + xline + ((y + yline) * uint8(64))] ^= uint8(1)
                    xline += uint16(1)
                yline += uint16(1)
            self.draw_flag = True

        elif self.opcode & 0xF0FF == 0xE09E:
            print("0xE09E")
            if self.keys[self.V[X(self.opcode)]] == uint8(1):
                self.PC += uint16(2)

        elif self.opcode & 0xF0FF == 0xE0A1:
            print("0xE0A1")
            if not self.keys[self.V[X(self.opcode)]] == uint8(1):
                self.PC += uint16(2)

        elif self.opcode & 0xF0FF == 0xF007:
            print("0xF007")
            self.V[X(self.opcode)] = self.delay_timer

        elif self.opcode & 0xF0FF == 0xF00A:
            print("0xF00A")

        elif self.opcode& 0xF0FF == 0xF015:
            print("0xF015")
            self.delay_timer = self.V[X(self.opcode)]

        elif self.opcode & 0xF0FF == 0xF018:
            print("0xF018")
            self.sound_timer = self.V[X(self.opcode)]

        elif self.opcode & 0xF0FF == 0xF01E:
            print("0xF01E")
            self.I += self.V[X(self.opcode)]

        elif self.opcode & 0xF0FF == 0xF029:
            print("0xF029")
            self.I = uint16(5) * self.V[X(self.opcode)]

        elif self.opcode & 0xF0FF == 0xF033:
            print("0xF033")
            self.memory[self.I] = self.V[X(self.opcode)] / uint8(100)
            self.memory[self.I + uint16(1)] = (self.V[X(self.opcode)] / uint8(10)) % uint8(10)
            self.memory[self.I + uint16(2)] = self.V[X(self.opcode)] % uint8(10)

        elif self.opcode & 0xF0FF == 0xF055:
            print("0xF055")
            index = uint16(0)
            while index <= X(self.opcode):
                self.memory[self.I + index] = self.V[index]
                index += uint16(1)

        elif self.opcode & 0xF0FF == 0xF065:
            print("0xF065")
            index = uint16(0)
            while index <= X(self.opcode):
                self.V[index] = self.memory[self.I + index]
                index += uint16(1)

        else:
            print("Invalid Opcode", self.opcode)
            return False
        
        return True