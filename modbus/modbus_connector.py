#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Modbus TCP: Implementation of Modbus TCP/IP protocol in python

 (C)2014 - Rasmus Letterkrantz - Rasmus.Letterkrantz@gmail.com

 This is distributed under the MIT license (MIT), see LICENSE.txt
"""

import socket, struct
from modbus.exceptions import *

class ModbusConnector():

    def __init__(self, host='127.0.0.1', port=502, timeout=5.0):
        self._host = host
        self._port = port
        self._timeout = timeout
        self._sock = None

    def __del__(self):
        self.disconnect()

    def connect(self):
        if self._sock:
            self._sock.close()
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_timeout(self._timeout)
        self._sock.connect((self._host, self._port))

    def disconnect(self):
        if self._sock:
            self._sock.close()
            self._sock = None

    def set_timeout(self, timeout):
        if timeout:
            self._timeout = timeout
            if self._sock:
                self._sock.setblocking(self._timeout > 0)
                self._sock.settimeout(self._timeout)

    def send(self, request):
        try:
            self.flush_socket(self._sock, 3)
        except Exception:
            self.connect()
        self._sock.send(request)

    def receive(self):
        result_bytes = str.encode("")
        limit = 0
        while len(result_bytes) < 6:
            rcv_byte = self._sock.recv(1)
            if rcv_byte:
                result_bytes += rcv_byte
            else:
                break
        if len(result_bytes) == 6:
            (tr_id, pr_id, to_be_recv_length) = struct.unpack(">HHH", result_bytes)
            limit = to_be_recv_length + 6
        while len(result_bytes) < limit:
            rcv_byte = self._sock.recv(1)
            if rcv_byte:
                result_bytes += rcv_byte
            else:
                break
        if len(result_bytes) < 9:
            raise ModbusInvalidResponseError("Not enough bytes to parse a response")
        return result_bytes
