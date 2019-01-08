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
        self.opcode = np.bitwise_or(np.left_shift(self.memory[self.PC], 8), self.memory[self.PC])
        print(self.opcode)
        return True