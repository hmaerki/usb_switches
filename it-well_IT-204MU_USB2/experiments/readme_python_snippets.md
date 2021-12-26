
from machine import Pin

leds = [Pin(p, Pin.OUT) for p in (6, 7, 8, 9)]

[led.value(1) for led in leds]
[led.value(0) for led in leds]


--------------------------------


from machine import Pin

buttons = [Pin(p, Pin.IN, Pin.PULL_UP) for p in (2, 3, 4, 5)]
[button.irq(lambda pin: print("IRQ with flags:", pin, pin.irq().flags()), Pin.IRQ_FALLING) for button in buttons]

--------------------------------
from machine import Pin, Timer

class Port:
  def __init__(self, gpio):
    self.led = Pin(gpio+4, Pin.OUT)
    self.button = Pin(gpio, Pin.IN, Pin.PULL_UP)
    self.gpio = gpio

  @property
  def pressed(self):
    return self.button.value() != 0
    
  def on(self, gpio):
    self.led.value(gpio == self.gpio)

class Switch:
  def __init__(self):
    self.ports = [Port(gpio) for gpio in (2, 3, 4, 5)]

  def tick(self):
    active_port = 0
    for port in self.ports:
      if port.pressed:
        active_port = port.gpio
    for port in self.ports:
      port.on(active_port)

switch = Switch()
timer = Timer() 	

timer.init(freq=2.5, mode=Timer.PERIODIC, callback=switch.tick)

