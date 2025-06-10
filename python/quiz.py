from machine import Pin
import time

gpio = [[0,1], [2,3]]

answered = False

class Button:
    def __init__(self, switch_pin, led_pin):
        self.switch_pin = Pin(switch_pin, Pin.IN, Pin.PULL_UP)
        self.led_pin = Pin(led_pin, Pin.OUT)
        self.led_pin.value(0)
        self.switch_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.switch_callback)

    def switch_callback(self, pin):
        global answered
        if answered: return

        self.led_pin.value(1)  # Turn on LED
        answered = True

buttons = [Button(pair[0], pair[1]) for pair in gpio]

reset = Pin(4, Pin.IN, Pin.PULL_UP)

while True:
    time.sleep(0.2)
    if reset.value() == 0:  # Reset button pressed
        answered = False
        for button in buttons:
            button.led_pin.value(0)  # Turn off all LEDs
        time.sleep(0.5)  # Debounce delay
      
