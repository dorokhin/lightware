#!/usr/bin/env python
"""
Class for manipulate 4 channel i2c Krida Electronics dimmer
for Banana Pro board, may also work with Raspberry Pi

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND

The MIT License (MIT)
Copyright (c) 2016 Andrew Dorokhin
github.com/andrewnsk

REQUIRE:
smbus
$ sudo apt install python-smbus

USAGE:
save as dimmer.py or your_file_name.py
$chmod +x ./dimmer.py
$./dimmer.py channel_num dimming_value

"""
import argparse
import logging
logging.basicConfig(filename='/run/dimmer.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%d.%m.%Y %H:%M:%S ')

try:
    import smbus
except ImportError as e:
    logging.warning('Error: ' + str(e))


class KridaDimmer:
    try:
        bus = smbus.SMBus(3)
    except IOError as e:
        logging.warning('Error: ' + str(e))
    except NameError as e:
        logging.warning('Error: ' + str(e))

    """
    Send one byte of data to the i2c dimmer.
    :param address: hex value of i2c address (replace with your dimmer address)
    :param channel_number: number of channel (decimal range from 1 to 4)
    :param level: dimming level, decimal range from 0 (Full On) to 100 (Full Off)
    """
    def __init__(self, address=0x27, channel_number=1, level=50):
        """
        Send one byte of control data to the i2c dimmer
        :param address: hex value of i2c address (replace with your dimmer address)
        :param channel_number: number of channel (decimal range from 1 to 4)
        :param level: dimming level, decimal range from 0 (Full On) to 100 (Full Off)
        """

        self._ADDRESS = address
        self._CHANNEL_ADDR = 0x7F + channel_number    # 0x80 (0x7F + 1)  1-st channel, ... ,  0x83 4-th channel
        self._LEVEL = level

    def write_byte(self):
        """Send one byte of data to the i2c dimmer.
        first byte is channel address
        second byte is dimming value
        """
        self.bus.write_byte(self._ADDRESS, self._CHANNEL_ADDR)
        self.bus.write_byte(self._ADDRESS, self._LEVEL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("channel", help="channel num", type=int)
    parser.add_argument("value", help="dimming value", type=int)
    args = parser.parse_args()
    logging.info('Set channel {0} to value {1}'.format(args.channel, args.value))

    dim = KridaDimmer(channel_number=args.channel, level=args.value)
    dim.write_byte()
