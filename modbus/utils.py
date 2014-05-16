#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Modbus TCP: Implementation of Modbus TCP/IP protocol in python

 (C)2014 - Rasmus Letterkrantz - Rasmus.Letterkrantz@gmail.com

 This is distributed under the MIT license (MIT), see LICENSE.txt
"""

import threading, select

def threadsafe_function(fcn):
    lock = threading.Lock()
    def new(*args, **kwargs):
        lock.acquire()
        try:
            ret = fcn(*args, **kwargs)
        except Exception as excpt:
            raise excpt
        finally:
            lock.release()
        return ret
    return new

def flush_socket(sockets, limit=0):
    """remove the data present on the socket"""
    input_socks = [sockets]
    count = 0
    while True:
        i_socks, o_socks, e_socks = select.select(input_socks, input_socks, input_socks, 0.0)
        if len(i_socks) == 0:
            break
        for sock in i_socks:
            sock.recv(1024)
        if limit>0:
            count += 1
        if count>=limit:
            raise Exception("socket is flushed maximum number of tries")