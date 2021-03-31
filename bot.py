from functions import *
from lib.InterceptionWrapper import InterceptionMouseState, InterceptionMouseStroke
import cv2
import numpy as np
import random

class Bot:

    def __init__(self, autohot_py):
        self.autohot_py = autohot_py
        self.step = 0
        self.window_info = get_window_info()
        self.useless_steps = 0

    def set_default_camera(self):
        self.autohot_py.PAGE_DOWN.press()
        time.sleep(0.2)
        self.autohot_py.PAGE_DOWN.press()
        time.sleep(0.2)
        self.autohot_py.PAGE_DOWN.press()

    def go_somewhere(self):
        """
        click to go
        """
        self.set_default_camera()
        smooth_move(self.autohot_py, 900, 650)  # @TODO dynamic
        stroke = InterceptionMouseStroke()
        stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
        self.autohot_py.sendToDefaultMouse(stroke)
        stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
        self.autohot_py.sendToDefaultMouse(stroke)
        self.set_default_camera()

    def turn2(self):
        """
        turn right
        """
        time.sleep(0.02)
        smooth_move(self.autohot_py, 300, 500)  # @TODO dynamic
        stroke = InterceptionMouseStroke()
        stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_RIGHT_BUTTON_DOWN
        time.sleep(0.1)
        self.autohot_py.sendToDefaultMouse(stroke)
        smooth_move(self.autohot_py, 345, 500)  # @TODO dynamic
        time.sleep(0.12)
        stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_RIGHT_BUTTON_UP
        self.autohot_py.sendToDefaultMouse(stroke)

    def turn(self):
        """
        turn right
        """
        time.sleep(0.02)
        self.autohot_py.RIGHT_ARROW.down()
        time.sleep(random.uniform(0.51, 0.69))
        self.autohot_py.RIGHT_ARROW.up()
        time.sleep(random.uniform(0.21, 0.39))


    def need_heal(self):
        img1 = get_screen(
            self.window_info["x"] + 195,
            self.window_info["y"] + 35,
            self.window_info["x"] + 250,
            self.window_info["y"] + 75
        )
        hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
        # lower red
        #   lower_green = array([36, 50, 50])
        #   upper_green = array([86, 255, 255])
        lower_green = array([36, 150, 150])
        upper_green = array([65, 230, 230])

        lower_blue = array([98, 109, 20])
        upper_blue = array([112, 255, 255])

        mask = cv2.inRange(hsv, lower_green, upper_green)
        mask1 = cv2.inRange(hsv, lower_blue, upper_blue)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 2))
        closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 2))
        closed1 = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, kernel1)

        if count_nonzero(closed) and count_nonzero(closed1):
            return 0
        elif count_nonzero(closed) and not count_nonzero(closed1):
            print('need mana')
            return 1
        elif not count_nonzero(closed) and count_nonzero(closed1) or not count_nonzero(closed) and not count_nonzero(closed1):
            print('need hp')
            return 2
        return -1


    def get_targeted_hp(self):
        """
        return victim's hp
        or -1 if there is no target
        """

        # target hp place img
        img_hp = get_screen(self.window_info["x"] + 605, self.window_info["y"] + 25,
                            self.window_info["x"] + 800,
                            self.window_info["y"] + 70)
        img_mana = get_screen(self.window_info["x"] + 605, self.window_info["y"] + 42,
                              self.window_info["x"] + 800,
                              self.window_info["y"] + 85)
        hsv_hp = cv2.cvtColor(img_hp, cv2.COLOR_BGR2HSV)
        hsv_mana = cv2.cvtColor(img_mana, cv2.COLOR_BGR2HSV)

        lower_red = array([0, 150, 150])
        upper_red = array([10, 200, 200])

        lower_orange = array([20, 100, 160])
        upper_orange = array([27, 255, 255])

        lower_blue = array([100, 160, 170])
        upper_blue = array([112, 255, 255])

        mask = cv2.inRange(hsv_hp, lower_red, upper_red)
        mask1 = cv2.inRange(hsv_mana, lower_blue, upper_blue)

        mask2 = cv2.inRange(hsv_hp, lower_orange, upper_orange)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 2))
        closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 2))
        closed1 = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, kernel1)

        kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 2))
        closed2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernel2)
        # if have mana and hp
        if count_nonzero(closed1) and (count_nonzero(closed) or count_nonzero(closed2)):
            return 1
        return -1

    def set_target(self):
        """
        find target and click
        """
        img = get_screen(self.window_info["x"], self.window_info["y"] + 100,
                         self.window_info["x"] + self.window_info["width"],
                         self.window_info["y"] + self.window_info["height"] - 300)
        cnts = get_target_centers(img)
        for cnt in range(len(cnts)):
            cent_x = cnts[cnt][0]
            cent_y = cnts[cnt][1] + 100
            # find target near hp icon and click
            iterator = 30
            while iterator < 120:
                img1 = get_screen(self.window_info["x"] + self.window_info["width"] * 0.75,
                                  self.window_info["y"] + self.window_info["height"] * 0.75,
                                  self.window_info["x"] + self.window_info["width"],
                                  self.window_info["y"] + self.window_info["height"])
                hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

                lower_red = array([0, 150, 150])
                upper_red = array([10, 200, 200])
                mask = cv2.inRange(hsv, lower_red, upper_red)
            #    res = cv2.bitwise_and(img1, img1, mask=mask)

                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 2))
                closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
             #   time.sleep(random.uniform(0.08, 0.15))
                if count_nonzero(closed) > 250:
                    if self.click_target():
                        return True
                smooth_move(
                    self.autohot_py,
                    cent_x,
                    cent_y + iterator
                )
                time.sleep(random.uniform(0.02, 0.06))
                iterator += random.randint(5, 11)
        return False

    def click_target(self):
        time.sleep(random.uniform(0.02, 0.03))
        stroke = InterceptionMouseStroke()
        stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
        self.autohot_py.sendToDefaultMouse(stroke)
        stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
        self.autohot_py.sendToDefaultMouse(stroke)
        if self.get_targeted_hp() <= 0:
            self.autohot_py.S.press()
            time.sleep(0.1)
            return 0
        time.sleep(random.uniform(0.02, 0.03))
        stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
        self.autohot_py.sendToDefaultMouse(stroke)
        stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
        self.autohot_py.sendToDefaultMouse(stroke)
        time.sleep(0.4)
        if self.get_targeted_hp() > 0:
            return 1
        self.autohot_py.S.press()
        time.sleep(0.1)
        return 0

    def find_loot(self):

        # loot if see loot.png icon
        template = cv2.imread('img/loot.png', 0)

        # print template.shape
        roi = get_screen(
            self.window_info["x"] + self.window_info["width"] * 0.3,
            self.window_info["y"] + self.window_info["height"] * 0.5,
            self.window_info["x"] + self.window_info["width"] * 0.7,
            self.window_info["y"] + self.window_info["height"] * 0.8
        )

        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        ret, th1 = cv2.threshold(roi, 224, 255, cv2.THRESH_TOZERO_INV)
        ret, th2 = cv2.threshold(th1, 135, 255, cv2.THRESH_BINARY)
        ret, tp1 = cv2.threshold(template, 224, 255, cv2.THRESH_TOZERO_INV)
        ret, tp2 = cv2.threshold(tp1, 135, 255, cv2.THRESH_BINARY)
        if not hasattr(th2, 'shape'):
            return False
        wth, hth = th2.shape
        wtp, htp = tp2.shape
        if wth > wtp and hth > htp:
            res = cv2.matchTemplate(th2, tp2, cv2.TM_CCORR_NORMED)
            if res.any():
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if max_val > 0.8:
                    self.autohot_py.F.press()
                    print('loot :)')
                    return True
                else:
                    return False
        return False



    def on_cd(self, file, is_combo=0, timer=0):
        template = cv2.imread(f'skills/{file}.png', 4)
        img = get_screen(self.window_info["x"] + 450, self.window_info["y"] + 700,
                         self.window_info["x"] + self.window_info["width"] - 450,
                         self.window_info["y"] + self.window_info["height"])
        is_in = cv2.matchTemplate(template, img, cv2.TM_CCORR_NORMED)
        if is_in.any():
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(is_in)
            if max_val > 0.99:
                return self.press_butt(file)
            if file == 3:
                return self.on_cd(31, is_combo, timer)
            elif file == 31:
                return self.on_cd(32, is_combo, timer)
        if is_combo != 0 and timer <= 61.1:
            timer += 0.055
            time.sleep(0.055)
            return self.on_cd(file, is_combo, timer)
        return 0

    def press_butt(self, file, is_combo=0):
        if file == 1:
            # shift + 1 Удар щитом
            self.autohot_py.LEFT_SHIFT.down()
            self.autohot_py.sleep()
            self.autohot_py.N1.down()
            self.autohot_py.sleep()
            self.autohot_py.LEFT_SHIFT.up()
            self.autohot_py.N1.up()
            return 1
        elif file == 2:
            # shift + 2 Раскол земли
            self.autohot_py.LEFT_SHIFT.down()
            self.autohot_py.sleep()
            self.autohot_py.N2.down()
            self.autohot_py.sleep()
            self.autohot_py.LEFT_SHIFT.up()
            self.autohot_py.N2.up()
        elif file == 3 or file == 31 or file == 32:
            # 1 Тройной удар
            self.autohot_py.N1.press()
        elif file == 4:
            # 2 Подавление
            self.autohot_py.N2.press()
        elif file == 5:
            # 3 Решающий удар
            self.autohot_py.N3.press()
        elif file == 6:
            # 4 Рывок
            self.autohot_py.N4.press()
        elif file == 7:
            # 5 Лассо
            self.autohot_py.N5.press()
        elif file == 8:
            # shift + 6 Адреналин
            self.autohot_py.LEFT_SHIFT.down()
            self.autohot_py.sleep()
            self.autohot_py.N6.down()
            self.autohot_py.sleep()
            self.autohot_py.LEFT_SHIFT.up()
            self.autohot_py.N6.up()
        elif file == 9:
            # 7 Непрерывное исцеление
            self.autohot_py.N7.press()
        elif file == 10:
            # 8 Дар жизни
            self.autohot_py.N8.press()
        elif file == 11:
            # 9 Заживление ран
            self.autohot_py.N9.press()
        elif file == 12:
            # 0 Клич жизни
            self.autohot_py.N0.press()
        elif file == 13:
            # - Глухая оборона
            self.autohot_py.DASH.press()
        elif file == 14:
            # + Доспехи мести
            self.autohot_py.BRACKET_LEFT.press()
        elif file == 15:
            # shift + 7 Жертвенный огонь
            self.autohot_py.LEFT_SHIFT.down()
            self.autohot_py.sleep()
            self.autohot_py.N7.down()
            self.autohot_py.sleep()
            self.autohot_py.LEFT_SHIFT.up()
            self.autohot_py.N7.up()
        elif file == 16:
            # shift + 8 Свет и тьма
            self.autohot_py.LEFT_SHIFT.down()
            self.autohot_py.sleep()
            self.autohot_py.N8.down()
            self.autohot_py.sleep()
            self.autohot_py.LEFT_SHIFT.up()
            self.autohot_py.N8.up()
        elif file == 17:
            # shift + 9 Массовое исцеление
            self.autohot_py.LEFT_SHIFT.down()
            self.autohot_py.sleep()
            self.autohot_py.N9.down()
            self.autohot_py.sleep()
            self.autohot_py.LEFT_SHIFT.up()
            self.autohot_py.N9.up()
        elif file == 18:
            # shift + 3 Победный клич
            self.autohot_py.LEFT_SHIFT.down()
            self.autohot_py.sleep()
            self.autohot_py.N3.down()
            self.autohot_py.sleep()
            self.autohot_py.LEFT_SHIFT.up()
            self.autohot_py.N3.up()
        elif file == 18:
            # shift + 4 Лассо
            self.autohot_py.LEFT_SHIFT.down()
            self.autohot_py.sleep()
            self.autohot_py.N4.down()
            self.autohot_py.sleep()
            self.autohot_py.LEFT_SHIFT.up()
            self.autohot_py.N4.up()
        else:
            print('not a skill', print(file))
            return 0
        return 1