from machine import Pin, Timer

class Port:
    def __init__(self, gpio):
        self.led = Pin(gpio+6, Pin.OUT)
        self.button = Pin(gpio+2, Pin.IN, Pin.PULL_UP)
        self.gpio = gpio

    @property
    def pressed(self):
        return self.button.value() == 0
        
    def on(self, gpio):
        self.led.value(gpio == self.gpio)

class Switch:
    def __init__(self):
        self.ports = [Port(gpio) for gpio in range(4)]
        self.active_port = 0

    def tick(self, timer):
        for port in self.ports:
            if port.pressed:
                self.active_port = port.gpio
            port.on(self.active_port)

switch = Switch()
while True:
    switch.tick(42)
# timer = Timer()     

# timer.init(freq=2.5, mode=Timer.PERIODIC, callback=switch.tick)

