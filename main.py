import esp32
from machine import Pin, PWM, deepsleep
import time
import _thread
import math

switch_signal_pin = Pin(36, Pin.IN)  # Will be used to wake up
led_pin = 23
buzzer_pin = PWM(Pin(22, Pin.OUT))

active_mode_duration = 10

tones = {
"B0": 31,
"C1": 33,
"CS1": 35,
"D1": 37,
"DS1": 39,
"E1": 41,
"F1": 44,
"FS1": 46,
"G1": 49,
"GS1": 52,
"A1": 55,
"AS1": 58,
"B1": 62,
"C2": 65,
"CS2": 69,
"D2": 73,
"DS2": 78,
"E2": 82,
"F2": 87,
"FS2": 93,
"G2": 98,
"GS2": 104,
"A2": 110,
"AS2": 117,
"B2": 123,
"C3": 131,
"CS3": 139,
"D3": 147,
"DS3": 156,
"E3": 165,
"F3": 175,
"FS3": 185,
"G3": 196,
"GS3": 208,
"A3": 220,
"AS3": 233,
"B3": 247,
"C4": 262,
"CS4": 277,
"D4": 294,
"DS4": 311,
"E4": 330,
"F4": 349,
"FS4": 370,
"G4": 392,
"GS4": 415,
"A4": 440,
"AS4": 466,
"B4": 494,
"C5": 523,
"CS5": 554,
"D5": 587,
"DS5": 622,
"E5": 659,
"F5": 698,
"FS5": 740,
"G5": 784,
"GS5": 831,
"A5": 880,
"AS5": 932,
"B5": 988,
"C6": 1047,
"CS6": 1109,
"D6": 1175,
"DS6": 1245,
"E6": 1319,
"F6": 1397,
"FS6": 1480,
"G6": 1568,
"GS6": 1661,
"A6": 1760,
"AS6": 1865,
"B6": 1976,
"C7": 2093,
"CS7": 2217,
"D7": 2349,
"DS7": 2489,
"E7": 2637,
"F7": 2794,
"FS7": 2960,
"G7": 3136,
"GS7": 3322,
"A7": 3520,
"AS7": 3729,
"B7": 3951,
"C8": 4186,
"CS8": 4435,
"D8": 4699,
    "DS8": 4978
    }

# cry_tone = ["F2","E2","DS2","B2","E2","B2","A2","G2"]
cry_tone = ["F6"] # Disabled as the sound quality is not great with a buzzer... might have to use a speaker instead.

def playtone(frequency):
    buzzer_pin.duty_u16(1000)
    buzzer_pin.freq(frequency)

def bequiet():
    buzzer_pin.duty_u16(0)

def cry(tone, sec:int = 5):
    for i in range(len(tone)):
        if (tone[i] == "P"):
            bequiet()
        else:
            playtone(tones[tone[i]])
        time.sleep(0.15)
    bequiet()

def intense_light(sec):
    pass
# 
class Light:
    def __init__(self, pin:int):
        self.light = PWM(Pin(pin, Pin.OUT))
        self.light.duty(512)
    
    def intensive(self, sec:int = 5):
        self.light.freq(10)
        time.sleep(sec)
        self.light.freq(5000)
        self.relax()
    
    def relax(self, ms:int = 60000):
        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) <= ms:
            duty = int((math.sin(time.ticks_ms() / 500) + 1 ) * 512)
            self.light.duty(duty)
            time.sleep_ms(10)
        self.light.duty(1023)
    
    def sleep(self):
        self.light.off()
            
def rage(sec:int = 5):
    light = Light(led_pin)
    _thread.start_new_thread(light.intensive,())
    _thread.start_new_thread(cry, [cry_tone])

def main():
    esp32.wake_on_ext0(pin = switch_signal_pin, level = esp32.WAKEUP_ANY_HIGH)
    
    awake = 20
    print(f"Im awake. Going to sleep in {awake} seconds")
    rage(awake)
    time.sleep(awake)
    print('Going to sleep now')
    deepsleep()
    

if __name__ == "__main__":
    print("ESP32 initialized")
    main()
