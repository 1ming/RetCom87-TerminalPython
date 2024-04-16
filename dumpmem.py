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

# parse the memory dump text file and convert it to a binary
# not the most robust but works for this purpose
def convert_to_binary(input_file, output_file):
    fh_out = open(output_file, "wb")
    with open(input_file, "r") as fh_in:
        for line in fh_in.readlines():
            # consider any line that starts with 00: valid for processing
            if line.startswith("00:"):
                # create a string of only the hex values with no spaces in between to be turned into a byte array
                data = "".join(line.split()[1:])
                line_bytes = bytearray.fromhex(data)
                fh_out.write(line_bytes)
    fh_out.close()

if __name__ == "__main__":
    PORT = "/dev/cu.usbserial-A10LVXS7"
    rc = RetCom87(port=PORT)
    rc.start_sequence()

    # first, dump memory from a location and store in a text file
    memory_dump(rc, "00:E000", "00:FFFF", save_file="monitor.txt", verbose=True)

    # parse the text file and convert it to a binary
    convert_to_binary("monitor.txt", "monitor.bin")