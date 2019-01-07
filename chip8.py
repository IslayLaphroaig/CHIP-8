from ctypes import c_ubyte, create_string_buffer, c_ushort

class Chip8:

    def __init__(self):
        self.opcode = c_ushort(0)
        self.memory = create_string_buffer(4096)
        self.V = create_string_buffer(16)
        self.I = c_ushort(0)
        self.PC = c_ushort(0x200)
        self.stack = create_string_buffer(16)
        self.stack_pointer = c_ushort(0)
        self.delay_timer = c_ubyte(0)
        self.sound_timer = c_ubyte(0)
        self.keys = create_string_buffer(16)
        self.display = create_string_buffer(64 * 32)
        
    def load_rom(self, rom):
        with open(rom, "rb") as r:
            address = 0x200
            byte = r.read(1)
            while byte:
                self.memory[address] = byte[0]
                byte = r.read(1)
                print(byte)