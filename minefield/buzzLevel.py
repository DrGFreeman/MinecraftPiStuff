from gpiozero import Buzzer
import threading
import time


class BuzzLevel:

    def __init__(self):
        self.buzzer = Buzzer(4)
        self.onTime = .01
        self.offTime = .19
        self.level = 0
        self.active = False
        self.run()

    def beep(self, on):
        if on:
            self.buzzer.on()
            time.sleep(self.onTime)
            self.buzzer.off()
            time.sleep(self.offTime)
        else:
            time.sleep(self.onTime + self.offTime)

    def beepLevel(self):
        for i in range(self.level):
            self.beep(True)
        for i in range(5 - self.level):
            self.beep(False)

    def run(self):
        thread1 = threading.Thread(target = self._run, args = [])
        thread1.start()

    def _run(self):
        self.active = True
        while self.active:
            self.beepLevel()

    def setLevel(self, level):
        self.level = level

    def stop(self):
        self.active = False
    
