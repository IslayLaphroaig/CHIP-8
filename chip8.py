from ctypes import *

class Chip8:

    def __init__(self):
        self.opcode = c_ushort()
        self.memory = bytearray(4096)
        self.V = bytearray(16)
        self.I = c_ushort()
        self.PC = c_ushort(0x200)
        self.stack = bytearray(16)
        self.stack_pointer = c_ushort()
        self.delay_timer = c_ubyte()
        self.sound_timer = c_ubyte()
        self.keys = bytearray(16)
        self.display = bytearray(64 * 32)
        print(self.memory)
        
    def load_rom(self, rom):
        with open(rom, "rb") as r:
            address = 0x200
            byte = r.read(1)
            while byte:
                self.memory[address] = byte[0]
                byte = r.read(1)
                print(byte)