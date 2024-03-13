# esp32_tyranitar

The ESP32-Tyranitar project is centered around the widely-used and budget-friendly microcontroller, ESP32, aiming to breathe life into one of Generation 2's iconic Pokémon, Tyranitar. Upon activation through a simple tap on the model, Tyranitar unleashes its distinctive cry sound, accompanied by a dynamic display of intense flickering lights, showcasing the characteristic of this pokemon based on it's description.

The code is written in micropython.

https://github.com/qmffkem/esp32_tyranitar/assets/28370250/34cd1a42-3154-4d06-8a5c-29a06fe389b5

## Features
* <b>ESP32 microcontroller:</b> Versatile microcontroller for small IOT project that's perfect for controlling various hardware modules with saving power consumption with the deep sleep mode.

* <b>Sensor Integration:</b> Utilize tap sensor for interactivity and is used to trigger to mode to wake up from deep sleep mode.

* <b>Lighting Effects:</b> Intense flickering of multiple red LEDs upon waking up from deep sleep mode, followed by gentle breathing effect.

* <b>Sound Generation:</b> Plays iconic cry of pokemon, Tyranitar upon waking up from deep sleep mode.


## Hardwares
1. ESP32
2. [Mini metal speaker](https://www.adafruit.com/product/1890)
3. [Max98357 I2S Amplifier Breakout](https://www.adafruit.com/product/3006)
3. [Tap sensor](https://arduinomodules.info/ky-031-knock-sensor-module/)
4. 3mm red LED diodes (x4)
5. 100 ohm resistor (for red LEDs)
. AA-3V junction box for battery
6. wires
7. [3D printed Tyranitar by 3dfux](https://www.thingiverse.com/thing:2821276)


## GPIO Pins
ESP32 pin out is based on [espressif page](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/_images/esp32-devkitC-v4-pinout.png).
| Usage      | PINs |
|------------|------|
| tap sensor | 36   |
| LED        | 23   |
| I2S: SCK   | 26   |
| I2S: WS    | 25   |
| I2S: SD    | 22   |

## Resources
I2S implementation to play music is based on [micropython-i2s-examples](https://github.com/miketeachman/micropython-i2s-examples) by @miketeachman.
