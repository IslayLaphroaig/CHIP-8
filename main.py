import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from chip8 import Chip8

WIDTH = 64
HEIGHT = 32
MODIFIER = 15

def main():
    chip_8 = Chip8()
    chip_8.load_rom('Roms/PONG')

    if not glfw.init():
        return

    window = glfw.create_window(WIDTH * MODIFIER, HEIGHT * MODIFIER, "CHIP-8", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_framebuffer_size_callback(window, glViewport(0, 0, 64, 32))
    glfw.make_context_current(window)
    glfw.swap_interval(0)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, (WIDTH * MODIFIER), (HEIGHT * MODIFIER), 0)
    glMatrixMode(GL_MODELVIEW)
    glViewport(0, 0, (WIDTH * MODIFIER), (HEIGHT * MODIFIER))

    while not glfw.window_should_close(window):
        if not chip_8.emulate_cycle():
            break
        if chip_8.draw_flag == True:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            for y in range(32):
                for x in range(64):
                    if(chip_8.display[x + 64 * y] == 0):
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

if __name__ == "__main__":
    main()