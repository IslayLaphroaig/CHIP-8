class Chip8:
    memory = bytearray(4096)
    V = bytearray(16)
    I = bytearray(1)
    PC = 0x200
    stack = bytearray(16)
    stack_pointer = 0
    delay_timer = 0
    sound_timer = 0
    keys = bytearray(16)
    display = bytearray(2048)