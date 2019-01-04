class Chip8:

    def __init__(self):
        self.memory = bytearray(4096)
        self.V = bytearray(16)
        self.I = bytearray(1)
        self.PC = 0x200
        self.stack = bytearray(16)
        self.stack_pointer = 0
        self.delay_timer = 0
        self.sound_timer = 0
        self.keys = bytearray(16)
        self.display = bytearray(2048)

    def load_rom(self, rom):
        with open(rom, "rb") as r:
            byte = r.read(1)
            while byte:
                self.memory[self.PC] = byte[0]
                self.PC += 1
                byte = r.read(1)
                print(byte)