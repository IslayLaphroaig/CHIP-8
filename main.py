import glfw
from chip8 import Chip8

def main():

    chip_8 = Chip8()
    chip_8.load_rom('Roms/PONG')
    #print(chip_8.memory)
    chip_8.emulate_cycle()

    if not glfw.init():
        return

    window = glfw.create_window(640, 480, "CHIP-8", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        if not chip_8.emulate_cycle():
            break
        glfw.swap_buffers(window)
        glfw.poll_events()
    glfw.terminate()

if __name__ == "__main__":
    main()