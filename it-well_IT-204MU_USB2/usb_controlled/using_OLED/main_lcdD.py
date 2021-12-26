# Pico-self.lcd_114-1.14
# https://www.waveshare.com/wiki/Pico-self.lcd_114-1.14
# https://www.waveshare.com/w/upload/9/9c/Pico_LCD_code.zip

# Big fonts
# https://github.com/peterhinch/micropython-font-to-py/blob/master/writer/WRITER.md
# https://raw.githubusercontent.com/peterhinch/micropython-font-to-py/master/writer/freesans20.py
# https://raw.githubusercontent.com/peterhinch/micropython-font-to-py/master/writer/courier20.py
# https://raw.githubusercontent.com/peterhinch/micropython-font-to-py/master/writer/writer.py

from machine import Pin,PWM
import uos
import usys

import pico_lcd_114

import writer
import courier20
# import freesans20

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

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

        self.active_port = 1
        pwm = PWM(Pin(BL))
        pwm.freq(1000)
        pwm.duty_u16(32768)#max 65535
        pwm.duty_u16(20000)#max 65535

        self.lcd_114 = pico_lcd_114.LCD_1inch14()
        #color BRG
        self.lcd_114.fill(BLACK)

        self.lcd_114.show()
        self.lcd_114.text("Raspberry Pi Pico",60,40,self.lcd_114.red)
        self.lcd_114.text("PicoGo",60,60,self.lcd_114.green)
        self.lcd_114.text("Pico-self.lcd_114-1.14",60,80,self.lcd_114.blue)
        self.lcd_114.text("mpy %s %s" % (usys.version, uos.uname().release),60,100,0x0000)

        self.writer = writer.CWriter(self.lcd_114, font=courier20, fgcolor=WHITE, bgcolor=BLACK, verbose=False)
        self.lcd_114.show()
    
    def button_pressed(self, port):
        self.active_port = port
        self.update_labels()

    def set_color(self, port):
        assert 1 <= port <= 4
        fgcolor = GREEN if port == self.active_port else WHITE
        self.writer.setcolor(fgcolor=fgcolor, bgcolor=BLACK)

    def device(self, family, id):
        for row_idx, text in ((-2, family), (0, id)):
            row = (self.lcd_114.height + row_idx*self.writer.font.height())//2
            col = (self.lcd_114.width - self.writer.stringlen(text))//2
            writer.CWriter.set_textpos(self.lcd_114, row=row, col=col)
            self.writer.printstring(text)
        self.lcd_114.show()
 
    def show(self):
        self.lcd_114.show()

    def update_labels(self):
        self.label(1, 'zini')
        self.label(2, 'ziwin20')
        self.label(3, 'ws02')
        self.label(4, '-')
        self.show()

    def label(self, port, text):
        assert 1 <= port <= 4
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
    oled.device("MFLI", "dev3519")
    oled.update_labels()
