import glfw
from OpenGL.GL import (
    glBegin,
    glClear,
    glColor3f,
    glEnd,
    glVertex3f,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_QUADS,
)
from OpenGL.GLU import gluOrtho2D
from chip8 import Chip8

WIDTH = 64
HEIGHT = 32
MODIFIER = 15


def main():
    chip_8 = Chip8()
    chip_8.load_rom("../roms/PONG")

    def key_callback(window, key, scancode, action, mods):
        if key == glfw.KEY_1:
            chip_8.keys[0x1] = 1
        elif key == glfw.KEY_2:
            chip_8.keys[0x2] = 1
        elif key == glfw.KEY_3:
            chip_8.keys[0x3] = 1
        elif key == glfw.KEY_4:
            chip_8.keys[0x4] = 1
        elif key == glfw.KEY_Q:
            chip_8.keys[0x5] = 1
        elif key == glfw.KEY_W:
            chip_8.keys[0x6] = 1
        elif key == glfw.KEY_E:
            chip_8.keys[0x7] = 1
        elif key == glfw.KEY_R:
            chip_8.keys[0x8] = 1
        elif key == glfw.KEY_A:
            chip_8.keys[0x9] = 1
        elif key == glfw.KEY_S:
            chip_8.keys[0xA] = 1
        elif key == glfw.KEY_D:
            chip_8.keys[0xB] = 1
        elif key == glfw.KEY_F:
            chip_8.keys[0xC] = 1
        elif key == glfw.KEY_Z:
            chip_8.keys[0xD] = 1
        elif key == glfw.KEY_X:
            chip_8.keys[0xE] = 1
        elif key == glfw.KEY_C:
            chip_8.keys[0xF] = 1
        elif key == glfw.KEY_V:
            chip_8.keys[0x10] = 1
        return True

    if not glfw.init():
        return

    window = glfw.create_window(
        WIDTH * MODIFIER, HEIGHT * MODIFIER, "CHIP-8", None, None
    )
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)
    gluOrtho2D(0, (WIDTH * MODIFIER), (HEIGHT * MODIFIER), 0)

    while not glfw.window_should_close(window):
        chip_8.update_timers()
        if not chip_8.emulate_cycle():
            break
        if chip_8.draw_flag == True:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            for y in range(32):
                for x in range(64):
                    if chip_8.display[x + (64 * y)] == 0:
                        glColor3f(0.0, 0.0, 0.0)
                    else:
                        glColor3f(1.0, 1.0, 1.0)
                    glBegin(GL_QUADS)
                    glVertex3f((x * MODIFIER), (y * MODIFIER), 0.0)
                    glVertex3f((x * MODIFIER), (y * MODIFIER) + MODIFIER, 0.0)
                    glVertex3f((x * MODIFIER) + MODIFIER, (y * MODIFIER) + MODIFIER, 0.0)
                    glVertex3f((x * MODIFIER) + MODIFIER, (y * MODIFIER) + 0.0, 0.0)
                    glEnd()
            chip_8.draw_flag = False
        glfw.swap_buffers(window)
        glfw.poll_events()
    glfw.terminate()


main()