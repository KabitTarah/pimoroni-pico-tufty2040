from machine import Pin

from util.constants import Constants as c

class ButtonHandler:
    def __init__(self):
        self.pins = {
            "a": c.button_a.pin,
            "b": c.button_b.pin,
            "c": c.button_c.pin,
            "u": c.button_up.pin,
            "d": c.button_down.pin,
        }
        self.flags = {
            "a": False,
            "b": False,
            "c": False,
            "u": False,
            "d": False,
        }
        
        for pin in self.pins.values():
            pin.irq(trigger=Pin.IRQ_FALLING, handler=self._callback)
            
    def _callback(self, pin):
        for k, p in self.pins.items():
            if pin == p:
                self.flags[k] = True
    
    def get_flag(self, flag):
        return self.flags.get(flag, False)
    
    def get_flags(self):
        flags = []
        for k, p in self.flags.items():
            if p:
                flags.append(k)
        return flags
    
    def reset(self):
        for k in self.flags:
            self.flags[k] = False

