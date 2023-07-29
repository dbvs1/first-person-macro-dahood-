from pynput import keyboard, mouse
import threading
import time

class ScrollThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.is_scrolling = False

    def run(self):
        while True:
            while self.is_scrolling:
                mouse.Controller().scroll(0, 1)  # Scroll up
                time.sleep(0.01)
                mouse.Controller().scroll(0, -1)  # Scroll down
                time.sleep(0.01)

def on_press(key):
    global scroll_thread, is_x_pressed, is_ctrl_pressed
    if key == keyboard.Key.esc:
        scroll_thread.is_scrolling = False
    elif key == keyboard.KeyCode.from_char('x'):
        is_x_pressed = True
    elif key == keyboard.Key.ctrl:
        is_ctrl_pressed = True

    # Check if both Ctrl and X are pressed simultaneously
    if is_ctrl_pressed and is_x_pressed:
        scroll_thread.is_scrolling = False

def on_release(key):
    global scroll_thread, is_x_pressed, is_ctrl_pressed
    if key == keyboard.KeyCode.from_char('x'):
        is_x_pressed = False
        if not is_ctrl_pressed:
            scroll_thread.is_scrolling = not scroll_thread.is_scrolling
    elif key == keyboard.Key.ctrl:
        is_ctrl_pressed = False

scroll_thread = ScrollThread()
scroll_thread.start()

is_x_pressed = False
is_ctrl_pressed = False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
