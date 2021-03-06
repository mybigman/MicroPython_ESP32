# import LoRaDuplexCallback
# import LoRaPingPong
# import LoRaSender
# import LoRaReceiver
import config_lora
from sx127x import SX127x
from controller_esp32 import ESP32Controller


from machine import Pin
from time import sleep
from ssd1306_i2c import Display

import dht


def send(lora):

    sensor = dht.DHT11(Pin(17))

    counter = 0
    print("LoRa Sender")
    display = Display()

    while True:
        ident = "LoRa Sender"

        sleep(2)

        sensor.measure()

        temp = sensor.temperature()
        temp_conv = str('{:d} C'.format(temp))
        hum = sensor.humidity()
        hum_conv = str('{:d} %'.format(hum))

        payload = '{} {} ({})'.format(temp_conv, hum_conv, counter)

        #payload = 'Hello ({0})'.format(counter)

        # print("Sending packet: \n{}\n".format(payload))

        display.show_text_wrap(
            "{0}                     {1}                   RSSI: {2}".format(ident, payload, lora.packetRssi()), 2)

        # Mensagem a enviar pelo sx127x.py:
        lora.println(payload)

        counter += 1
        sleep(5)


controller = ESP32Controller()
lora = controller.add_transceiver(SX127x(name='LoRa'),
                                  pin_id_ss=ESP32Controller.PIN_ID_FOR_LORA_SS,
                                  pin_id_RxDone=ESP32Controller.PIN_ID_FOR_LORA_DIO0)


# LoRaDuplexCallback.duplexCallback(lora)
# LoRaPingPong.ping_pong(lora)
send(lora)
# LoRaReceiver.receive(lora)
