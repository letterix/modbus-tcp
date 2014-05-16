#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from modbus_tcp.modbus_tcp import ModbusTcp
from modbus_tcp.exceptions import *

if __name__ == "__main__":
    try:
        client = ModbusTcp(host = '192.168.0.1')
        print(client.read_holding_registers(5, 1))

    except ModbusError as e:
        print("%s- Code=%d" % (e, e.get_exception_code()))