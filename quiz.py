from machine import Pin
import time

# Switch/LED pairs
gpio = [[0,1], [2,3]]

# Global variable to track if the question has been answered
answered = False

class Button:
    def __init__(self, switch_pin, led_pin):
        """Initialize the button with a switch and an LED pin.  Finally register the switch callback."""
        self.switch_pin = Pin(switch_pin, Pin.IN, Pin.PULL_UP)
        self.led_pin = Pin(led_pin, Pin.OUT)
        self.led_pin.value(0)
        self.switch_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.switch_callback)

    def switch_callback(self, pin):
        """Callback function for switch press. Turns on the LED if the question has not been answered."""
        global answered
        if answered: return

        self.led_pin.value(1)  # Turn on LED
        answered = True

# Initialize buttons with GPIO pairs
buttons = [Button(pair[0], pair[1]) for pair in gpio]

# Reset button to reset the quiz
reset = Pin(4, Pin.IN, Pin.PULL_UP)

# Main loop to check for button presses and reset
while True:
    time.sleep(0.2)
    if reset.value() == 0:  # Reset button pressed
        answered = False
        for button in buttons:
            button.led_pin.value(0)  # Turn off all LEDs
        time.sleep(0.5)  # Debounce delay
      
