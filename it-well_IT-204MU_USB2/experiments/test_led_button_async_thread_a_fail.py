from machine import Pin
import uasyncio as asyncio
import _thread

# https://github.com/peterhinch/micropython-async
# https://forum.micropython.org/viewtopic.php?t=4867 async and thread

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
                self.led.value(False)
                return
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

def main(_dummy):
    loop = asyncio.get_event_loop()
    asyncio.create_task(switch.update())
    loop.run_forever()

# main(42)
_thread.start_new_thread(main, [42])
