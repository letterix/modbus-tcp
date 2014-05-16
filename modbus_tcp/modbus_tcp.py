#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Modbus TCP: Implementation of Modbus TCP/IP protocol in python

 (C)2014 - Rasmus Letterkrantz - Rasmus.Letterkrantz@gmail.com

 This is distributed under the MIT license (MIT), see LICENSE.txt
"""

from modbus_tcp.modbus_coder import ModbusCoder
from modbus_tcp.modbus_connector import ModbusConnector
from modbus_tcp.utils import threadsafe_function

class ModbusTcp:


    def __init__(self, host='127.0.0.1', port=502, timeout=5.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.modbus_coder = ModbusCoder()
        self.modbus_connector = ModbusConnector(host, port, timeout)

    @threadsafe_function
    def read_holding_registers(self, start_address, num_addresses, slave=1):
        request_bytes = self.modbus_coder.code_read_holding_register(start_address, slave, num_addresses)
        self.modbus_connector.connect()
        self.modbus_connector.send(request_bytes)
        response_bytes = self.modbus_connector.receive()
        return self.modbus_coder.decode_read_holding_register(response_bytes)
