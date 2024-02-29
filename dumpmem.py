#!/usr/bin/env python3

"""Script for dumping contents of memory into a file."""

import time
from pexpect import fdpexpect

from rcterm import RetCom87


# get memory dump within a range of addresses
def memory_dump(device, low, high, save_file="dump.txt", verbose=True):
    low_pair = [a.encode() for a in low.split(":")]
    high_pair = [a.encode() for a in high.split(":")]

    with fdpexpect.fdspawn(device) as reader:
        # request a memory dump and provide the low and high addresses
        reader.send(b"d")
        for first, second in (low_pair, high_pair):
            reader.expect(b"BB:AAAA")
            reader.send(first)
            reader.expect(b":")
            reader.send(second)
        time.sleep(1)

        # write output to a file
        device.write_output_file(save_file, verbose)


if __name__ == "__main__":
    PORT = "/dev/cu.usbserial-A10LVXS7"
    rc = RetCom87(port=PORT)
    rc.start_sequence()

    memory_dump(rc, "00:E000", "00:FFFF", save_file="monitor.txt", verbose=True)
    # memory_dump(rc, "00:0200", "00:1000", verbose=True)
