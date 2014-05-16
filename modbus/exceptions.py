#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Modbus TCP: Implementation of Modbus TCP/IP protocol in python

 (C)2014 - Rasmus Letterkrantz - Rasmus.Letterkrantz@gmail.com

 This is distributed under the MIT license (MIT), see LICENSE.txt
"""

class ModbusError(Exception):
    """Base error for the module. The exception codes is the error code returned by
    the slave in the response.
    """

    def __init__(self, exception_code, value=""):
        if not value:
            value = "Modbus Error: Exception code = %d" % exception_code
        Exception.__init__(self, value)
        self._exception_code = exception_code

    def get_exception_code(self):
        return self._exception_code


class ModbusInvalidResponseError(Exception):
    """
    Exception raised when the response sent by the slave doesn't fit
    with the expected format
    """
    pass


class ModbusInvalidMbapError(Exception):
    """
    Exception raised when the response sent by the slave doesn't fit
    with the expected format of the Mbap
    """
    pass


class ModbusInvalidPduError(Exception):
    """
    Exception raised when the response sent by the slave doesn't fit
    with the expected format of the Mbap
    """
    pass