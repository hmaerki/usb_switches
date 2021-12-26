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
import freesans20

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
        self.key0 = Pin(15,Pin.IN)
        self.key1 = Pin(17,Pin.IN)
        self.key2 = Pin(2 ,Pin.IN)
        self.key3 = Pin(3 ,Pin.IN)

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
    
    def set_color(self, port):
        assert 1 <= port <= 4
        fgcolor = GREEN if port == 2 else WHITE
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
    oled.label(1, 'zini')
    oled.label(2, 'ziwin20')
    oled.label(3, 'ws02')
    oled.label(4, '-')
    oled.device("MFLI", "dev3519")
    oled.show()
