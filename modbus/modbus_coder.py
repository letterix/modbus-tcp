#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Modbus TCP: Implementation of Modbus TCP/IP protocol in python

 (C)2014 - Rasmus Letterkrantz - Rasmus.Letterkrantz@gmail.com

 This is distributed under the MIT license (MIT), see LICENSE.txt
"""

import struct
from modbus.utils import threadsafe_function
from modbus.exceptions import *
from modbus import defines


class ModbusCoder():
    def __init__(self):
        self._request_pdu = Pdu()
        self._response_pdu = Pdu()
        self._request_mbap = Mbap()
        self._response_mbap = Mbap()

    @threadsafe_function
    def code_read_holding_register(self, start_address, slave=1, num_addresses=1):
        self._set_request_pdu(start_address, num_addresses)
        pdu = self._request_pdu.pack_bytes()
        self._set_request_mbap(slave, len(pdu), defines.FC_READ_HOLDING_REGISTER)
        mbap = self._request_mbap.pack_bytes()
        return mbap + pdu

    @threadsafe_function
    def decode_read_holding_register(self, response_bytes):
        self._reset_response_mbap()
        self._reset_response_pdu()
        mbap_bytes = response_bytes[:8]
        pdu_bytes = response_bytes[8:]
        self._response_mbap.unpack_bytes(mbap_bytes)
        return self._response_pdu.unpack_bytes(pdu_bytes, self._response_mbap.function_code)

    def _set_request_pdu(self, start_address, num_addresses):
        self._reset_request_pdu()
        self._request_pdu.set_start_address(start_address)
        self._request_pdu.set_num_registers(num_addresses)

    def _set_request_mbap(self, slave, pdu_length, function_code):
        self._reset_request_mbap()
        self._request_mbap.next_transaction_id()
        self._request_mbap.set_unit_id(slave)
        self._request_mbap.set_function_code(function_code)
        self._request_mbap.set_pdu_length(pdu_length)

    def _reset_request_mbap(self):
        """Needs to keep tracking the transaction_id"""
        self._request_mbap.__init__()

    def _reset_response_mbap(self):
        """No need to track transaction_id here"""
        self._response_mbap = Mbap()

    def _reset_request_pdu(self):
        self._request_pdu = Pdu()

    def _reset_response_pdu(self):
        self._response_pdu = Pdu()


#-----------------------------------------------------------------------------------------------------------------------


class Pdu:
    _PDU_REQUEST_ENCODING = '>HH'
    _PDU_RESPONSE_ENCODING = '>B'

    def __init__(self):
        self.start_address = 0
        self.num_registers = 0
        self.data = ()

    def set_start_address(self, start_address):
        self.start_address = start_address

    def set_num_registers(self, num_registers):
        self.num_registers = num_registers

    def pack_bytes(self):
        return struct.pack(self._PDU_REQUEST_ENCODING, self.start_address, self.num_registers)

    def unpack_bytes(self, bytes, return_code):
        second_byte = struct.unpack(Pdu._PDU_RESPONSE_ENCODING, bytes[0:1])
        if return_code > 0x80:
            # the slave has returned an error
            exception_code = second_byte[0]
            raise ModbusError(exception_code)
        else:
            data_length = second_byte[0]
            data_encoding = '>' + (int(data_length / 2) * 'H')
            data = bytes[1:]
            if len(data) != data_length:
                # the byte count in the pdu is invalid
                raise ModbusInvalidResponseError("Byte count is %d while actual number of bytes is %d. " \
                                                 % (data_length, len(data)))
            result = struct.unpack(data_encoding, data)
            return result


#-----------------------------------------------------------------------------------------------------------------------


class Mbap:
    _MBAP_ENCODING = '>HHHBB'

    transaction_id = 0

    def __init__(self):
        self.protocol_id = 0
        self.unit_id = 0
        self.function_code = 0
        self.pdu_length = 0

    def next_transaction_id(self):
        Mbap.transaction_id = (Mbap.transaction_id + 1) % 255
        return Mbap.transaction_id

    def set_pdu_length(self, pdu_length):
        self.pdu_length = pdu_length

    def set_unit_id(self, unit_id):
        self.unit_id = unit_id

    def set_function_code(self, function_code):
        self.function_code = function_code

    def pack_bytes(self):
        return struct.pack(Mbap._MBAP_ENCODING, self.transaction_id, self.protocol_id, self.pdu_length + 2,
                           self.unit_id, self.function_code)

    def unpack_bytes(self, bytes):
        (_, _, d_len, u_id, f_cd) = struct.unpack(Mbap._MBAP_ENCODING, bytes)
        self.set_pdu_length(d_len - 1)
        self.set_unit_id(u_id)
        self.set_function_code(f_cd)

