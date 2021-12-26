from machine import Pin
import uasyncio as asyncio

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

    async def on(self, idx):
        self._on = idx == self.idx

        for i in range(10):
            if not self._on:
                break
            await asyncio.sleep_ms(200)
            self.led.toggle()
        self.led.value(self._on)

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
        while True:
            await asyncio.sleep_ms(100)
            if idx == self.active_port:
                continue
            idx = self.active_port
            print("Button %d pressed" % idx)
            # Update LED blinking
            for port in self.ports:
                asyncio.create_task(port.on(self.active_port))
            # Update USB switch FET
            self.s0.value(self.active_port % 2)
            self.s1.value(self.active_port//2 % 2)

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

def test2():
    asyncio.create_task(switch.update())
    asyncio.run_forever()

def test1():
    loop = asyncio.get_event_loop()
    asyncio.create_task(switch.update())
    loop.run_forever()

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

test1()
