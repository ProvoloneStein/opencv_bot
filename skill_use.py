def on_cd(file):
    template = cv2.imread(f'skills/{file}.png', 0)
    window_info = get_window_info()
    img = get_screen(window_info["x"] + 450, window_info["y"] + 700,
                     window_info["x"] + window_info["width"] - 450,
                     window_info["y"] + window_info["height"])



def find_loot(self):
    # shift + 1 Удар щитом
    #1png
    template = cv2.imread('skills/1.png', 0)
    autohotpy.LEFT_SHIFT.down()
    autohotpy.sleep()
    autohotpy.N1.down()
    autohotpy.sleep()
    autohotpy.LEFT_SHIFT.up()
    autohotpy.N1.up()
    # shift + 2 Раскол земли
    template = cv2.imread('skills/2.png', 0)
    autohotpy.LEFT_SHIFT.down()
    autohotpy.sleep()
    autohotpy.N2.down()
    autohotpy.sleep()
    autohotpy.LEFT_SHIFT.up()
    autohotpy.N2.up()
    # 1 Тройной удар
    template = cv2.imread('skills/3.png', 0)
    autohot_py.N1.press()
    # 2 Подавление
    template = cv2.imread('skills/4.png', 0)
    # 1png
    # shifr + 1 Удар щитом
    # 1png
    # shifr + 1 Удар щитом
    # 1png
    # shifr + 1 Удар щитом
    # 1png
    # shifr + 1 Удар щитом
    # 1png
    # shifr + 1 Удар щитом
    # 1png
    # shifr + 1 Удар щитом
    # 1png
    # shifr + 1 Удар щитом
    # 1png
    # shifr + 1 Удар щитом
    # 1png
    # shifr + 1 Удар щитом
    # 1png # shifr + 1 Удар щитом
    #     #1png
    # shifr + 1 Удар щитом
    # 1png
    # shifr + 1 Удар щитом
    # 1png
    # shifr + 1 Удар щитом
    # 1png


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
            if max_val > 0.9:
                self.autohot_py.F.press()
                return True
            else:
                return False