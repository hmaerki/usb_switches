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
        # writer.CWriter.set_textpos(self.lcd_114, 0, 0)
        # self.writer.printstring('Sunday\n12 Aug 2018\n10.30am')

        row_top = 0
        row_bottom = self.lcd_114.height - self.writer.font.height()
        col_left = 0
        col_right = self.lcd_114.width - self.writer.font.max_width()

        writer.CWriter.set_textpos(self.lcd_114, row=row_top, col=col_left)
        self.writer.printstring("1")

        writer.CWriter.set_textpos(self.lcd_114, row=row_top, col=col_right)
        self.writer.printstring("2")

        writer.CWriter.set_textpos(self.lcd_114, row=row_bottom, col=col_left)
        self.writer.printstring("3")

        writer.CWriter.set_textpos(self.lcd_114, row=row_bottom, col=col_right)
        self.writer.printstring("4")

        self.lcd_114.show()


        self.lcd_114.show()
    
    def label_(self, i, text):
        if i in (0, 2):
            # Left
            _text = "%d %s" % (i+1, text)
            col = 0
        else:
            # Right
            _text = "%s %d" % (text, i+1)
            col = self.lcd_114.width - self.writer.stringlen(_text)
        if i in (0, 1):
            # Top
            row = 0
        else:
            # Bottom
            row = self.lcd_114.height - self.writer.font.height()
        writer.CWriter.set_textpos(self.lcd_114, row=row, col=col)
        self.writer.printstring(_text)
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
 
    def label(self, port, text):
        assert 1 <= port <= 4
        self.set_color(port)
        if port in (1, 3):
            # Left
            col = 0
        else:
            # Right
            col = self.lcd_114.width - self.writer.stringlen(text)
        if port in (1, 2):
            # Top
            row = self.writer.font.height()
        else:
            # Bottom
            row = self.lcd_114.height - 2*self.writer.font.height()
        writer.CWriter.set_textpos(self.lcd_114, row=row, col=col)
        self.writer.printstring(text)
        self.lcd_114.show()

if __name__=='__main__':
    oled = Oled()
    oled.label(1, 'zini')
    oled.label(2, 'ziwin20')
    oled.label(3, 'ws02')
    oled.label(4, '-')
    oled.device("MFLI", "dev3519")
