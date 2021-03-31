from functions import *
from bot import Bot

class Destroyer (Bot):

    def loop(self, stop_event):
        """
        main bot logic
        """
        while not stop_event.is_set():

            # check if looting needed
            self.find_loot()

            # check target hp
            targeted_hp = self.get_targeted_hp()
            if targeted_hp > 0:
                iteration = 0
                self.autohot_py.N1.down()
                self.autohot_py.sleep()
                while self.get_targeted_hp() > 0:
                 #  if (iteration % 5) == 1:
                 #       self.autohot_py.N1.up()
                 #       time.sleep(0.33)
                 #       self.autohot_py.N5.press()
                 #       self.on_cd(8)
                 #       self.on_cd(13)
                #        self.on_cd(14)
                #        self.autohot_py.N1.down()
                #        self.autohot_py.sleep()
                    #Комбо 1. Проверяем рывок на кнопке 4. далее даем удар щитом и бафаемся
                    if self.on_cd(6):
                        self.autohot_py.N1.up()
                        self.autohot_py.N4.press()
                        time.sleep(0.83)
                        self.on_cd(8)
                        time.sleep(0.03)
                        self.on_cd(13)
                        time.sleep(0.03)
                        self.on_cd(14)
                        time.sleep(0.03)
                        self.autohot_py.N3.press()
                        time.sleep(1.13)
                        self.autohot_py.LEFT_SHIFT.down()
                        self.autohot_py.sleep()
                        self.autohot_py.N8.press()
                        self.autohot_py.sleep()
                        self.autohot_py.LEFT_SHIFT.up()
                        self.autohot_py.N8.up()
                        time.sleep(0.78)
                        self.autohot_py.N1.down()
                        self.autohot_py.sleep()
                    #Комбо 2. Проверяем Подавление на кнопе 2 и бьем массами
                    if self.on_cd(4):
                        self.autohot_py.N1.up()
                        time.sleep(0.38)
                        self.autohot_py.N2.press()
                        time.sleep(0.78)
                        self.autohot_py.LEFT_SHIFT.down()
                        self.autohot_py.sleep()
                        self.autohot_py.N0.press()
                        self.autohot_py.sleep()
                        self.autohot_py.LEFT_SHIFT.up()
                        self.autohot_py.N0.up()
                        time.sleep(0.78)
                        self.autohot_py.LEFT_SHIFT.down()
                        self.autohot_py.sleep()
                        self.autohot_py.DASH.press()
                        self.autohot_py.sleep()
                        self.autohot_py.LEFT_SHIFT.up()
                        self.autohot_py.DASH.up()
                        time.sleep(0.78)
                        self.autohot_py.LEFT_SHIFT.down()
                        self.autohot_py.sleep()
                        self.autohot_py.N1.press()
                        self.autohot_py.sleep()
                        self.autohot_py.LEFT_SHIFT.up()
                        self.autohot_py.N1.up()
                        time.sleep(0.21)
                        self.autohot_py.LEFT_SHIFT.down()
                        self.autohot_py.sleep()
                        self.autohot_py.N1.press()
                        self.autohot_py.sleep()
                        self.autohot_py.LEFT_SHIFT.up()
                        self.autohot_py.N1.up()
                        self.autohot_py.N1.down()
                        self.autohot_py.sleep()
                    if self.need_heal() == 2:
                        print('healing')
                        self.autohot_py.N1.up()
                        time.sleep(0.15)
                        self.on_cd(12)
                        self.on_cd(11)
                        self.autohot_py.N1.down()
                        self.autohot_py.sleep()
                    iteration += 1
                    if iteration >= 750:
                        self.autohot_py.ESC.press()
                        break
                self.autohot_py.N1.up()
                self.find_loot()
                continue
            else:
                print("no target yet")
                self.autohot_py.N5.press()
                # check if you attack more than one target
                time.sleep(2.0)
                if self.get_targeted_hp() > 0:
                    print("oh... another one")
                    continue
                if self.need_heal() == 2:
                    print('afk_healing')
                    time.sleep(0.15)
                    self.on_cd(12)
                    self.on_cd(11)
                    if self.on_cd(9):
                        print("x5 heal")
                        self.autohot_py.N7.press()
                        time.sleep(0.02)
                        self.autohot_py.N7.press()
                        time.sleep(0.02)
                        self.autohot_py.N7.press()
                        time.sleep(0.02)
                        self.autohot_py.N7.press()
                        time.sleep(0.02)
                    self.on_cd(17)
                    time.sleep(random.uniform(2.51, 3.69))
                    continue
                elif self.need_heal() == 1:
                    print('healing mana')
                    self.autohot_py.N6.press()
                    time.sleep(random.uniform(2.51, 3.69))
                    continue
                # Find and click on the victim
                self.find_loot()
                if self.set_target():
                    if self.get_targeted_hp() > 0:
                        print("set_target - attack")
                    else:
                        print("missclick, sleep")
                        self.autohot_py.S.press()
                        time.sleep(3.22)
                    continue
         #   else:
                # Turn on
            self.turn()
            print("turn")

            print("next iteration")
            pass

        print("loop finished!")