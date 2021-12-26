# Pico-LCD-1.14
# https://www.waveshare.com/wiki/Pico-LCD-1.14
# https://www.waveshare.com/w/upload/9/9c/Pico_LCD_code.zip

# Big fonts
# https://github.com/peterhinch/micropython-font-to-py/blob/master/writer/WRITER.md
# https://raw.githubusercontent.com/peterhinch/micropython-font-to-py/master/writer/courier20.py
# https://github.com/peterhinch/micropython-font-to-py/blob/master/writer/writer.py

from machine import Pin,PWM
import uos
import usys

import pico_lcd_114

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

if __name__=='__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)#max 65535
    pwm.duty_u16(20000)#max 65535

    LCD = pico_lcd_114.LCD_1inch14()
    #color BRG
    LCD.fill(LCD.white)
 
    LCD.show()
    LCD.text("Raspberry Pi Pico",60,40,LCD.red)
    LCD.text("PicoGo",60,60,LCD.green)
    LCD.text("Pico-LCD-1.14",60,80,LCD.blue)
    LCD.text("mpy %s %s" % (usys.version, uos.uname().release),60,100,0x0000)
    LCD.show()
