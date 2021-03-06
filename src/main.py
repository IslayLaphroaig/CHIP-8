import glfw
from os import getcwd
from os import system
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
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from sys import platform
from chip8 import Chip8
if platform.startswith('win'):
    from winsound import Beep


DISPLAY_HEIGHT = 32
DISPLAY_WIDTH = 64
DISPLAY_MODIFIER = 15
FPS = 60.0
FREQUENCY = 1000
DURATION_WINDOWS = 100
DURATION_LINUX_MAC = 0.1


def main():
    Tk().withdraw()
    chip_8 = Chip8()
    chip_8.load_data("font_set", 0)
    chip_8.load_data(
        askopenfilename(
            initialdir=getcwd(),
            title="Select a CHIP-8 Rom",
            filetypes=(("Chip-8 Roms", "*.ch8"),),
        ),
        chip_8.pc,
    )
    Tk().destroy()

    def key_callback(window, key, scancode, action, mods):
        def key_1():
            chip_8.keys[0x0] = action == glfw.PRESS

        def key_2():
            chip_8.keys[0x1] = action == glfw.PRESS

        def key_3():
            chip_8.keys[0x2] = action == glfw.PRESS

        def key_4():
            chip_8.keys[0x3] = action == glfw.PRESS

        def key_q():
            chip_8.keys[0x4] = action == glfw.PRESS

        def key_w():
            chip_8.keys[0x5] = action == glfw.PRESS

        def key_e():
            chip_8.keys[0x6] = action == glfw.PRESS

        def key_r():
            chip_8.keys[0x7] = action == glfw.PRESS

        def key_a():
            chip_8.keys[0x8] = action == glfw.PRESS

        def key_s():
            chip_8.keys[0x9] = action == glfw.PRESS

        def key_d():
            chip_8.keys[0xA] = action == glfw.PRESS

        def key_f():
            chip_8.keys[0xB] = action == glfw.PRESS

        def key_z():
            chip_8.keys[0xC] = action == glfw.PRESS

        def key_x():
            chip_8.keys[0xD] = action == glfw.PRESS

        def key_c():
            chip_8.keys[0xE] = action == glfw.PRESS

        def key_v():
            chip_8.keys[0xF] = action == glfw.PRESS

        def exit_rom():
            quit()

        return {
            glfw.KEY_1: key_1,
            glfw.KEY_2: key_2,
            glfw.KEY_3: key_3,
            glfw.KEY_4: key_4,
            glfw.KEY_Q: key_q,
            glfw.KEY_W: key_w,
            glfw.KEY_E: key_e,
            glfw.KEY_R: key_r,
            glfw.KEY_A: key_a,
            glfw.KEY_S: key_s,
            glfw.KEY_D: key_d,
            glfw.KEY_F: key_f,
            glfw.KEY_Z: key_z,
            glfw.KEY_X: key_x,
            glfw.KEY_C: key_c,
            glfw.KEY_V: key_v,
            glfw.KEY_ESCAPE: exit_rom,
        }.get(key, lambda: None)()

    def draw():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(1.0, 1.0, 1.0)
        for y in range(32):
            for x in range(64):
                if chip_8.display[x + (64 * y)] == 1:
                    glBegin(GL_QUADS)
                    glVertex3f(
                        (x * DISPLAY_MODIFIER),
                        (y * DISPLAY_MODIFIER),
                        0.0,
                    )
                    glVertex3f(
                        (x * DISPLAY_MODIFIER),
                        (y * DISPLAY_MODIFIER) + DISPLAY_MODIFIER,
                        0.0,
                    )
                    glVertex3f(
                        (x * DISPLAY_MODIFIER) + DISPLAY_MODIFIER,
                        (y * DISPLAY_MODIFIER) + DISPLAY_MODIFIER,
                        0.0,
                    )
                    glVertex3f(
                        (x * DISPLAY_MODIFIER) + DISPLAY_MODIFIER,
                        (y * DISPLAY_MODIFIER) + 0.0,
                        0.0,
                    )
                    glEnd()

    if not glfw.init():
        return

    window = glfw.create_window(
        DISPLAY_WIDTH * DISPLAY_MODIFIER,
        DISPLAY_HEIGHT * DISPLAY_MODIFIER,
        "CHIP-8",
        None,
        None,
    )

    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)
    gluOrtho2D(
        0, (DISPLAY_WIDTH * DISPLAY_MODIFIER), (DISPLAY_HEIGHT * DISPLAY_MODIFIER), 0
    )

    last_time = glfw.get_time()

    while not glfw.window_should_close(window):
        while not chip_8.draw_flag:
            chip_8.update_timers()
            if chip_8.play_sound == True:
                if platform.startswith('win'):
                    Beep(FREQUENCY , DURATION_WINDOWS)
                elif platform.startswith('lin'):
                    system('play -nq -t alsa synth {} sine {}'.format(DURATION_LINUX_MAC, FREQUENCY))
                elif platform.startswith('dar'):
                    system('play -nq -t alsa synth {} sine {}'.format(DURATION_LINUX_MAC, FREQUENCY))
                chip_8.play_sound = False
                break
            if not chip_8.cycle():
                chip_8.draw_flag = True
                break
            if chip_8.draw_flag:
                while glfw.get_time() < last_time + 1.0 / FPS:
                    draw()
                    glfw.swap_buffers(window)
                last_time += 1.0 / FPS
        chip_8.draw_flag = False
        glfw.poll_events()
    glfw.terminate()


main()
