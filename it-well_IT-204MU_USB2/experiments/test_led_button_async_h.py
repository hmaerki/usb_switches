from machine import Pin
import uasyncio as asyncio

# https://github.com/peterhinch/micropython-async
import usys
from machine import Pin, Timer

class Port:
    def __init__(self, switch, idx):
        self.switch = switch
        self.led = Pin(idx+6, Pin.OUT)
        self.button = Pin(idx+2, Pin.IN, Pin.PULL_UP)
        self.idx = idx
        self.button.irq(self.irq_falling, Pin.IRQ_FALLING)

    def irq_falling(self, pin):
        # print("IRQ with flags:", pin, pin.irq().flags())
        self.switch.irq_button(self.idx)

    def on(self, idx):
        self.led.value(idx == self.idx)

    async def blink(self):
        for i in range(10):
            await asyncio.sleep_ms(200)
            self.led.toggle()


class Switch:
    def __init__(self):
        self.ports = [Port(self, idx) for idx in range(4)]
        self.active_port = 0
        self.s0 = Pin(0, Pin.OUT)
        self.s1 = Pin(1, Pin.OUT)

    def irq_button(self, idx):
        self.active_port = idx

    async def update(self):
        idx = -1
        task_blink = None
        while True:
            await asyncio.sleep_ms(100)
            if idx == self.active_port:
                continue
            idx = self.active_port
            print("new idx=%d" % idx)
            for port in self.ports:
                port.on(self.active_port)
                self.s0.value(self.active_port % 2)
                self.s1.value(self.active_port//2 % 2)
            
            if task_blink:
                task_blink.cancel()
            for port in self.ports:
                if port.idx == self.active_port:
                    task_blink = asyncio.create_task(port.blink())


switch = Switch()

async def killer(duration):
    await asyncio.sleep(duration)

async def toggle(port, time_ms):
    while True:
        await asyncio.sleep_ms(time_ms)
        port.led.toggle()

async def main(duration):
    print("Flash LED's for {} seconds".format(duration))

    # for port in switch.ports:
    #     t = 1000
    #     asyncio.create_task(toggle(port, t))
    asyncio.run(killer(duration))

def test(duration=10):
    print("A")
    asyncio.create_task(switch.update())
    asyncio.run()
    # asyncio.run(killer(duration))
    print("B")
    asyncio.new_event_loop()
    print("C")
    return
    try:
        asyncio.run(main(duration))
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        asyncio.new_event_loop()
        print('as_demos.aledflash.test() to run again.')

test()
