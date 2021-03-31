
import pywintypes
#import pythoncom # Uncomment this if some other DLL load will fail
import win32gui
from PIL import ImageOps, Image, ImageGrab
from numpy import *
import time
import cv2





# Brazenhem algo
def draw_line(x1=0, y1=0, x2=0, y2=0):

    coordinates = []

    dx = x2 - x1
    dy = y2 - y1

    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0

    if dx < 0:
        dx = -dx
    if dy < 0:
        dy = -dy

    if dx > dy:
        pdx, pdy = sign_x, 0
        es, el = dy, dx
    else:
        pdx, pdy = 0, sign_y
        es, el = dx, dy

    x, y = x1, y1

    error, t = el / 2, 0

    coordinates.append([x, y])

    while t < el:
        error -= es
        if error < 0:
            error += el
            x += sign_x
            y += sign_y
        else:
            x += pdx
            y += pdy
        t += 1
        coordinates.append([x, y])

    return coordinates


# Smooth move mouse from current pos to xy
def smooth_move(autohotpy, x, y):
    flags, hcursor, (startX, startY) = win32gui.GetCursorInfo()
    coordinates = draw_line(startX, startY, x, y)
    x = 0
    for dot in coordinates:
        x += 1
        if x % 2 == 0 and x % 3 == 0:
            time.sleep(0.005)
        autohotpy.moveMouseToPosition(dot[0], dot[1])


def get_window_info():
    # set window info
    window_info = {}
    win32gui.EnumWindows(set_window_coordinates, window_info)
    return window_info


# EnumWindows handler
# sets L2 window coordinates
def set_window_coordinates(hwnd, window_info):
    if win32gui.IsWindowVisible(hwnd):
        if WINDOW_SUBSTRING in win32gui.GetWindowText(hwnd):
            rect = win32gui.GetWindowRect(hwnd)
            x = rect[0]
            y = rect[1]
            w = rect[2] - x
            h = rect[3] - y
            window_info['x'] = x
            window_info['y'] = y
            window_info['width'] = w
            window_info['height'] = h
            window_info['name'] = win32gui.GetWindowText(hwnd)
            win32gui.SetForegroundWindow(hwnd)


def get_screen(x1, y1, x2, y2):
    box = (x1 + 8, y1 + 30, x2 - 8, y2)
    screen = ImageGrab.grab(box)
    open_cv_image = array(screen)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    return open_cv_image


def get_target_centers(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # lower red
    lower_red = array([0, 100, 100])
    upper_red = array([10, 200, 200])
    # upper_red = array([10,255,255])


    mask = cv2.inRange(hsv, lower_red, upper_red)
    kernel = ones((5, 5), uint8)
    closed = cv2.erode(mask, kernel, iterations=1)

    cv2.imwrite('res.jpg', closed)
    centers, hierarchy = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    centr = []
    for cnt in centers:
        if cv2.contourArea(cnt) > 30:
            M = cv2.moments(cnt)
            cX = int(M['m10'] / M["m00"])
            cY = int(M['m01'] / M["m00"])
            centr.append([cX, cY])

    return centr
