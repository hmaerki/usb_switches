# minicom -o -D /dev/ttyACM0
# cat /dev/ttyACM0 &
# echo -n -e "button(1)\r" >  /dev/ttyACM0
# echo -n -e "button()\r" >  /dev/ttyACM0

# Features to add
#
# Switch-counter
# Reboot-counter
# Store state to flash
# Make sure, state is restored after watchdog
# watchdog
# commands with CRC

import sys
from machine import Pin

# https://github.com/peterhinch/micropython-async

class Port:
    def __init__(self, switch, idx):
        self._on = False
        self.switch = switch
        self.idx = idx
        self.led = Pin(idx+6, Pin.OUT)
        button = Pin(idx+2, Pin.IN, Pin.PULL_UP)
        button.irq(self.irq_falling, Pin.IRQ_FALLING)

    def irq_falling(self, pin):
        self.switch.irq_button(self.idx)

    def update_led(self):
        self.led.value(self.switch.active_port == self.idx)

class Switch:
    def __init__(self):
        self.ports = [Port(self, idx) for idx in range(4)]
        self.active_port = 0
        self.active_port_last = -1
        self.s0 = Pin(0, Pin.OUT)
        self.s1 = Pin(1, Pin.OUT)
        self.irq_button(0)

    def irq_button(self, idx):
        self.active_port = idx
        if self.active_port_last == self.active_port:
            return
        self.active_port_last = self.active_port
        print("button(%d) # Button pressed" % idx)
        # Update LED blinking
        for port in self.ports:
            port.update_led()
        # Update USB switch FET
        self.s0.value(self.active_port % 2)
        self.s1.value(self.active_port//2 % 2)


switch = Switch()

def button(idx=None):
    switch.irq_button(idx)
    
def get():
    print("button(%d)" % switch.active_port)
    
while True:
    line = sys.stdin.readline().strip()
    try:
        eval(line)
    except Exception as e:
        print("error %s" % e)

