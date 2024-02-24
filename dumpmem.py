#!/usr/bin/env python3

"""Script for dumping contents of memory into a file."""

import time

import pexpect
from pexpect import fdpexpect

from rcterm import RetCom87

MAX_READ_BYTES = 256


def request_data():
    low = "00:0200"
    high = "00:0300"

    # request memory dump `d`
    rc.write_message(b"d")
    rc.read_until("BB:AAAA")

    # send low address in two parts

    # send high address in two parts

    # receive data until we are done


if __name__ == "__main__":
    PORT = "/dev/cu.usbserial-A10LVXS7"
    rc = RetCom87(port=PORT)
    rc.start_sequence()

    reader = fdpexpect.fdspawn(rc)
    reader.send(b'd')
    state = reader.expect(b'BB:AAAA')
    reader.send(b'00')
    reader.expect(b':')
    reader.send(b'0200')
    reader.expect(b'BB:AAAA')
    reader.send(b'00')
    reader.expect(b':')
    reader.send(b'0400')
    time.sleep(1)

    max_bytes = 256
    fh = open("test.txt", "wb")

    while rc.in_waiting > 0:
      bytes_to_read = rc.in_waiting
      bytes_to_read = max_bytes if bytes_to_read > max_bytes else bytes_to_read
      data = rc.read(bytes_to_read)
      print(f"Read {len(data)} bytes")
      print(data)
      fh.write(data)
      time.sleep(0.1)

    fh.close()
    print()
