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
        def key_1():
            chip_8.keys[0x0] = action == glfw.PRESS

        def key_2():
            chip_8.keys[0x1] = action == glfw.PRESS

        def key_3():
            chip_8.keys[0x2] = action == glfw.PRESS

        def key_4():
            chip_8.keys[0x3] = action == glfw.PRESS

        def key_Q():
            chip_8.keys[0x4] = action == glfw.PRESS

        def key_W():
            chip_8.keys[0x5] = action == glfw.PRESS

        def key_E():
            chip_8.keys[0x6] = action == glfw.PRESS

        def key_R():
            chip_8.keys[0x7] = action == glfw.PRESS

        def key_A():
            chip_8.keys[0x8] = action == glfw.PRESS

        def key_S():
            chip_8.keys[0x9] = action == glfw.PRESS

        def key_D():
            chip_8.keys[0xA] = action == glfw.PRESS

        def key_F():
            chip_8.keys[0xB] = action == glfw.PRESS

        def key_Z():
            chip_8.keys[0xC] = action == glfw.PRESS

        def key_X():
            chip_8.keys[0xD] = action == glfw.PRESS

        def key_C():
            chip_8.keys[0xE] = action == glfw.PRESS

        def key_V():
            chip_8.keys[0xF] = action == glfw.PRESS

        return {
            glfw.KEY_1: key_1,
            glfw.KEY_2: key_2,
            glfw.KEY_3: key_3,
            glfw.KEY_4: key_4,
            glfw.KEY_Q: key_Q,
            glfw.KEY_W: key_W,
            glfw.KEY_E: key_E,
            glfw.KEY_R: key_R,
            glfw.KEY_A: key_A,
            glfw.KEY_S: key_S,
            glfw.KEY_D: key_D,
            glfw.KEY_F: key_F,
            glfw.KEY_Z: key_Z,
            glfw.KEY_X: key_X,
            glfw.KEY_C: key_C,
            glfw.KEY_V: key_V,
        }.get(key, lambda: None)()

    def draw():
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
    glfw.swap_interval(0)
    gluOrtho2D(0, (WIDTH * MODIFIER), (HEIGHT * MODIFIER), 0)

    while not glfw.window_should_close(window):
        chip_8.update_timers()
        if not chip_8.emulate_cycle():
            break
        if chip_8.draw_flag == True:
            draw()
            chip_8.draw_flag = False
        glfw.swap_buffers(window)
        glfw.poll_events()
    glfw.terminate()


main()
