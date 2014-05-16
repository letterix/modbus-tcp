#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from modbus.modbus_tcp import ModbusTcp
from modbus import utils
from modbus.exceptions import *
logger = utils.create_logger("console")

if __name__ == "__main__":
    try:
        logger.info("test started")
        client = ModbusTcp(host = '192.168.0.1')
        logger.info(client.read_holding_registers(5, 1))

    except ModbusError as e:
        logger.error("%s- Code=%d" % (e, e.get_exception_code()))