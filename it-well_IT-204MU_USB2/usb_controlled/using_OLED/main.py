# Pico-self.lcd_114-1.14
# https://www.waveshare.com/wiki/Pico-self.lcd_114-1.14
# https://www.waveshare.com/w/upload/9/9c/Pico_LCD_code.zip

# Big fonts
# https://github.com/peterhinch/micropython-font-to-py/blob/master/writer/WRITER.md
# https://raw.githubusercontent.com/peterhinch/micropython-font-to-py/master/writer/freesans20.py
# https://raw.githubusercontent.com/peterhinch/micropython-font-to-py/master/writer/courier20.py
# https://raw.githubusercontent.com/peterhinch/micropython-font-to-py/master/writer/writer.py
#
#
# Commands
# echo "get()" > /dev/ttyACM0
# echo "button(4)" > /dev/ttyACM0
# echo "set_labels(('linux12', 'win7', 'win10', '-'))" > /dev/ttyACM0
# echo "set_device('UHF', 'dev88')" > /dev/ttyACM0
# 


from machine import Pin,PWM
import uos
import usys

import pico_lcd_114

import writer
import courier20
# import freesans20

BL = 13  # Backlight

# color BRG
WHITE = 0xffff
BLACK = 0x0000
GREEN = 0x001f

class Oled:
    def __init__(self):
        def button(pin, handler):
            p = Pin(pin, Pin.IN)
            p.irq(handler=handler, trigger=Pin.IRQ_FALLING, hard=False)
            return p

        button(15, lambda pin: self.button_pressed(1))  # Label on PCB: KEY0
        button(17, lambda pin: self.button_pressed(3))  # Label on PCB: KEY1
        button(2, lambda pin: self.button_pressed(2))  # Label on PCB: KEY2
        button(3, lambda pin: self.button_pressed(4))  # Label on PCB: KEY4

        self.labels = (
            'zini',
            'ziwin20',
            'ws02',
            '-',
        )
        self.dev_family = 'MFLI'
        self.dev_id = 'dev3519'
        self.active_port = 1
        pwm = PWM(Pin(BL))
        pwm.freq(1000)
        pwm.duty_u16(65535)  # max 65535

        self.lcd_114 = pico_lcd_114.LCD_1inch14()
        self.writer = writer.CWriter(self.lcd_114, font=courier20, fgcolor=WHITE, bgcolor=BLACK, verbose=False)

    def button_pressed(self, port, silent=False):
        last_active_port = self.active_port
        self.active_port = port
        self.update_label(last_active_port)
        self.update_label(self.active_port)
        oled.show()

        if not silent:
            print("button(%d)" % port)

    def set_color(self, port):
        assert 1 <= port <= 4
        fgcolor = GREEN if port == self.active_port else WHITE
        self.writer.setcolor(fgcolor=fgcolor, bgcolor=BLACK)

    def update_dev(self):
        self.writer.setcolor(fgcolor=GREEN, bgcolor=BLACK)

        for row_idx, text in ((-2, self.dev_family), (0, self.dev_id)):
            row = (self.lcd_114.height + row_idx*self.writer.font.height())//2
            col = (self.lcd_114.width - self.writer.stringlen(text))//2
            writer.CWriter.set_textpos(self.lcd_114, row=row, col=col)
            self.writer.printstring(text)
 
    def show(self):
        self.lcd_114.show()

    def clear_and_update_all(self):
        self.lcd_114.fill(BLACK)
        self.update_labels()
        self.update_dev()
        self.writer.setcolor(fgcolor=WHITE, bgcolor=BLACK)
        self.lcd_114.text("v%s" % uos.uname().release, 60, 128, GREEN)
        self.show()

    def update_labels(self):
        for port0, update_label in enumerate(self.labels):
            self.update_label(port0+1)

    def update_label(self, port):
        assert 1 <= port <= 4
        text = self.labels[port-1]
        self.set_color(port)
        if port in (1, 3):
            # Left
            col = 0
            col_label = 0
        else:
            # Right
            col = self.lcd_114.width - self.writer.stringlen(text)
            col_label = self.lcd_114.width - self.writer.font.max_width()
        if port in (1, 2):
            # Top
            row = self.writer.font.height()
            row_label = 0
        else:
            # Bottom
            row = self.lcd_114.height - 2*self.writer.font.height()
            row_label = self.lcd_114.height - self.writer.font.height()
        writer.CWriter.set_textpos(self.lcd_114, row=row, col=col)
        self.writer.printstring(text)
        writer.CWriter.set_textpos(self.lcd_114, row=row_label, col=col_label)
        self.writer.printstring(str(port))

if __name__=='__main__':
    oled = Oled()
    oled.clear_and_update_all()

    def button(port):
        oled.button_pressed(port, silent=True)
        
    def get():
        print("button(%d)" % oled.active_port)

    def set_labels(labels):
        if len(labels) != 4:
            print("ERROR: 4 labels are required")
            return

        oled.labels = labels
        oled.clear_and_update_all()

    def set_device(family, dev_id):
        oled.dev_family = family
        oled.dev_id = dev_id
        oled.clear_and_update_all()

    while True:
        line = usys.stdin.readline().strip()
        if len(line) == 0:
            continue
        try:
            eval(line)
        except Exception as e:
            print("error %s" % e)
