import esp32
from machine import Pin, PWM, deepsleep, DAC, I2S
import time
import _thread
import math

# wake up sensor configuration
WAKE_UP_PIN = 36  # Will be used to wake up

# LED configuration
LED_PIN = 23  # PINs for LED

# I2S configuration
SCK_PIN = 26  # I2S PINs for speaker
WS_PIN = 25  # I2S PINs for speaker
SD_PIN = 22  # I2S PINs for speaker
I2S_ID = 0
BUFFER_LENGTH_IN_BYTES = 5000

# Audio configuration
CRY_FILE = "248_tyranitar.wav"  # File to play
WAV_SAMPLE_SIZE_IN_BITS = 32
FORMAT = I2S.STEREO
SAMPLE_RATE_IN_HZ = 24000


class Light:
    def __init__(self, pin: int = LED_PIN):
        self.light = PWM(Pin(pin, Pin.OUT))
        self.light.duty(512)

    def intensive(self, sec: int = 5):
        self.light.freq(10)
        time.sleep(sec)
        self.light.freq(5000)
        self.relax()

    def relax(self, ms: int = 60000):
        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) <= ms:
            duty = int((math.sin(time.ticks_ms() / 500) + 1) * 512)
            self.light.duty(duty)
            time.sleep_ms(10)
        self.light.duty(1023)

    def sleep(self):
        self.light.off()


class Pokemon:
    def __init__(
        self,
        name: str = None,
        uptime: int = 20,
        cry_file: str = None,
    ):

        # variables
        self.name = name
        self.uptime = uptime
        self.cry_file = cry_file

        # AUDIO
        self.audio_out = I2S(
            I2S_ID,
            sck=Pin(SCK_PIN),
            ws=Pin(WS_PIN),
            sd=Pin(SD_PIN),
            mode=I2S.TX,
            bits=WAV_SAMPLE_SIZE_IN_BITS,
            format=FORMAT,
            rate=SAMPLE_RATE_IN_HZ,
            ibuf=BUFFER_LENGTH_IN_BYTES,
        )

        # LED
        self.light = Light(LED_PIN)

    def awake(self):
        _thread.start_new_thread(self.cry, ())
        _thread.start_new_thread(self.light.intensive, ())

    def cry(self):
        # file validation
        if not self.cry_file:
            raise ValueError("No cry file provided")
        if not self.cry_file.endswith(".wav"):
            raise ValueError("File must be a .wav file")

        wav = open(self.cry_file, "rb")
        wav.seek(44)  # Skip the header

        wav_samples = bytearray(1000)
        wav_samples_mv = memoryview(wav_samples)

        num_read = wav.readinto(wav_samples_mv)
        while num_read:
            self.audio_out.write(wav_samples_mv[:num_read])
            num_read = wav.readinto(wav_samples_mv)


def main():
    tyranitar = Pokemon(name="Tyranitar", uptime=20, cry_file=CRY_FILE)

    # pin to wake up from deep sleep mode
    esp32.wake_on_ext0(pin=Pin(WAKE_UP_PIN, Pin.IN), level=esp32.WAKEUP_ANY_HIGH)

    # action after wake up
    tyranitar.awake()
    time.sleep(tyranitar.uptime)

    # deep sleep to save battery
    deepsleep()


if __name__ == "__main__":
    print("ESP32 initialized")
    main()
