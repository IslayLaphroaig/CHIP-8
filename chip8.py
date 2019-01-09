import numpy as np

class Chip8:

    np.set_printoptions(threshold=np.nan) # for debugging
    np.set_printoptions(formatter={'int':lambda x:hex(int(x))}) # for debugging

    font_set = np.array([
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
            ], dtype=np.uint8)

    def __init__(self):
        self.opcode = np.uint16(0)
        self.memory = np.zeros(4096, dtype=np.uint8)
        self.V = np.zeros(16, dtype=np.uint8)
        self.I = np.uint16(0)
        self.PC = np.uint16(0x200)
        self.stack = np.zeros(16, dtype=np.uint8)
        self.stack_pointer = np.uint16(0)
        self.delay_timer = np.uint8(0)
        self.sound_timer = np.uint8(0)
        self.keys = np.zeros(16, dtype=np.uint8)
        self.display = np.zeros(64 * 32, dtype=np.uint8)
        self.memory = np.insert(self.memory, 0x50, self.font_set, axis=0)

    def load_rom(self, rom):
        data = np.fromfile(rom, dtype=np.uint8)
        self.memory = np.insert(self.memory, 0x200, data, axis=0)

    def emulate_cycle(self):
        # fetch opcode
        self.opcode = np.bitwise_or(np.left_shift(self.memory[self.PC], np.uint16(8)), self.memory[self.PC])
        print(self.opcode)

        #decode opcode
        if(np.bitwise_and(self.opcode, 0xF000)) == 0x0000:
            print("0x0000")

        elif(self.opcode == 0x00E0):
            print("0x00E0")

        elif(self.opcode == 0x00EE):
            print("0x00EE")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0x1000:
            print("0x1000")    

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0x2000:
            print("0x2000")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0x3000:
            print("0x3000")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0x4000:
            print("0x4000")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0x5000:
            print("0x5000")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0x6000:
            print("0x6000")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0x7000:
            print("0x7000")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0x8000:
            print("0x8000")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0x8001:
            print("0x8001")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0x8002:
            print("0x8002")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0x8003:
            print("0x8003")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0x8004:
            print("0x8004")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0x8005:
            print("0x8005")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0x8006:
            print("0x8006")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0x8007:
            print("0x8007")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0x8008:
            print("0x8008")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0x9000:
            print("0x9000")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0xA000:
            print("0xA000")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0xB000:
            print("0xB000")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0xC000:
            print("0xC000")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0xD000:
            print("0xD000")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0xE09E:
            print("0xE09E")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0xE0A1:
            print("0xE0A1")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0xF007:
            print("0xF007")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0xF00A:
            print("0xF00A")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0xF015:
            print("0xF015")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0xF018:
            print("0xF018")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0xF01E:
            print("0xF01E")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0xF029:
            print("0xF029")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0xF033:
            print("0xF033")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0xF055:
            print("0xF055")

        elif(np.bitwise_and(self.opcode, 0xF00)) == 0xF065:
            print("0xF065")

        else:
            print("Invalid Opcode")
            return False
        
        return True