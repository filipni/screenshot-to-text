import pyautogui
import pytesseract
from PIL import Image, ImageGrab
from pynput import keyboard, mouse


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
mouse_controller = mouse.Controller()
screenshot_boundary = []


def on_release(key):
    if (hasattr(key, 'char')):
        return

    if key.name == 'print_screen':
        print('Enter boundary')
        screenshot_boundary.clear()
    elif key.name == 'esc':
        print('Exiting application')
        exit(0)


def on_click(x, y, button, pressed):
    if pressed:
        return

    if button == mouse.Button.left and len(screenshot_boundary) < 2:
        mouse_pos = (x, y)
        screenshot_boundary.append(mouse_pos)
        print(mouse_pos)
        validate_boundary()
    elif button == mouse.Button.middle and len(screenshot_boundary) == 2:
        mouse_controller.click(mouse.Button.left)
        text = screenshot_and_get_text()
        paste(text)


def validate_boundary():
    if (len(screenshot_boundary) != 2):
        return

    (x1, y1) = screenshot_boundary[0]
    (x2, y2) = screenshot_boundary[1] 
    
    valid = x1 <= x2 and y1 <= y2

    if not valid:
        print('Boundary not valid, try again')
        screenshot_boundary.clear()
    else:
        print('Boundary updated') 


def screenshot_and_get_text():
    (x1, y1) = screenshot_boundary[0]
    (x2, y2) = screenshot_boundary[1]

    image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    image_text = pytesseract.image_to_string(image)

    return image_text


def paste(text):
    pyautogui.typewrite(text)
    pyautogui.keyDown('enter')


def main():
    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    keyboard_listener = keyboard.Listener(on_release=on_release)
    keyboard_listener.start()

    print("Enter boundary")
    keyboard_listener.join()


if __name__ == '__main__':
    main()
