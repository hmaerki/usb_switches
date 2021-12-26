from machine import Pin
import uasyncio as asyncio

# https://github.com/peterhinch/micropython-async
import usys
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
        self.s0 = Pin(0, Pin.OUT)
        self.s1 = Pin(1, Pin.OUT)

    def tick(self, timer):
        for port in self.ports:
            if port.pressed:
                self.active_port = port.gpio
            port.on(self.active_port)
            self.s0.value(self.active_port % 2)
            self.s1.value(self.active_port//2 % 2)

switch = Switch()
# while True:
#     switch.tick(42)
#     print("Hallo")
#     x = usys.stdin.readline()
#     print("Received %d characters >%s<" % (len(x), x))
# timer = Timer()     

# timer.init(freq=2.5, mode=Timer.PERIODIC, callback=switch.tick)

async def killer(duration):
    await asyncio.sleep(duration)

async def toggle(port, time_ms):
    while True:
        await asyncio.sleep_ms(time_ms)
        port.led.toggle()

async def main(duration):
    print("Flash LED's for {} seconds".format(duration))

    for port in switch.ports:
        t = 1000
        asyncio.create_task(toggle(port, t))
    asyncio.run(killer(duration))

def test(duration=10):
    try:
        asyncio.run(main(duration))
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        asyncio.new_event_loop()
        print('as_demos.aledflash.test() to run again.')

test()
