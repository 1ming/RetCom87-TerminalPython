#!/usr/bin/env python3

import sys
import time
import argparse
import readline  # to make input() handle backspace
import serial
from serial.tools import list_ports


class RetCom87(serial.Serial):
    DEFAULT_END_SEQUENCE = b"\r>"
    STARTUP_END_SEQUENCE = b"\r\r>"
    MAX_READ_BYTES = 256

    def __init__(self, port, baudrate=9600, timeout=5, show_raw=False, **kwargs):
        self.show_raw = show_raw
        # currently using the same value for both read and write timeouts
        super().__init__(
            port, baudrate, timeout=timeout, write_timeout=timeout, **kwargs
        )

    # print some config info and instructions
    # detect monitor startup message
    # using this is optional, can also skip to a read/write loop
    # i have this separate because the startup message sometimes comes as
    # 1 byte followed by the rest after a couple seconds
    # while subsequent data seems to come through much faster
    def start_sequence(self):
        self.reset_input_buffer()
        self.reset_output_buffer()
        print(f"Using port: {self.portstr}")
        print(f"Baudrate: {self.baudrate}")
        print(f"Press the reset button to begin.")

        # keep trying to read the monitor startup until we see it
        while True:
            # crude check for the startup message
            # this end sequence here only seems to appear after reset
            message = self.read_until(self.STARTUP_END_SEQUENCE)
            if "MENSCH" in message.decode():
                self.print_formatted(message)
                break

    # pyserial uses io library's readline() which can only use \n as the delimeter
    # this one uses \r instead
    def _readline(self):
        return self.read_until(b"\r")

    # general purpose read with delay
    # this one just tries to read however many bytes are waiting
    def simple_read(self):
        total_bytes_read = 0
        data = b""
        while self.in_waiting > 0:
            data += self.read(self.in_waiting)
            total_bytes_read += len(data)
            time.sleep(0.1)  # wait a bit in case there's more data coming
        print(f"Bytes read: {total_bytes_read}")
        self.print_formatted(data)
        return data

    def write_message(self, message):
        if len(message) == 0:
            # send newline if we pressed enter without typing anything
            send_data = b"\r"
        else:
            send_data = message.encode()
        print(f"Sending: {send_data}")
        bytes_written = self.write(send_data)
        print(f"Bytes sent: {bytes_written}")
        print()

    # general purpose read/write loop
    def simple_loop(self):
        self.write_prompt()
        while True:
            if self.in_waiting > 0:
                self.simple_read()
                self.write_prompt()

    def write_prompt(self, prompt_text="Command (hit enter to send): "):
        out_data = input(prompt_text)
        self.write_message(out_data)

    # print a cleaned up version of a message received from board
    def print_formatted(self, message):
        print()
        if self.show_raw:
            print("==RAW OUTPUT==")
            print(message)
        else:
            print("==OUTPUT==")
            lines = [a.strip() for a in message.decode().split("\r")]
            for line in lines:
                print(line)
        print("===")
        print()

    # write the output from the device to a file
    def write_output_file(self, save_file="output.txt", verbose=True):
        print(f"Writing output to file: {save_file}")
        with open(save_file, "wb") as fh:
            while self.in_waiting > 0:
                bytes_to_read = self.in_waiting
                bytes_to_read = (
                    self.MAX_READ_BYTES
                    if bytes_to_read > self.MAX_READ_BYTES
                    else bytes_to_read
                )
                data = self.read(bytes_to_read)
                if verbose:
                    print(f"Read {len(data)} bytes")
                    print(data)
                fh.write(data)
                time.sleep(0.1)
        print("Writing complete.")


# get the first device matching the pattern
def find_device():
    # could just use \w+ here instead
    # i set it to >2 for now because there's other entries on my computer
    for p in list_ports.grep(r"cu\.usbserial-\w{2,}"):
        return p.device
    return None


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="""Basic serial interface for RetCom87""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-p",
        "--port",
        dest="port",
        default=None,
        help="Serial port of the board. If not specified, it will pick the first one it detects.",
    )
    parser.add_argument(
        "-b",
        "--baudrate",
        type=int,
        default=9600,
        dest="baudrate",
        help="Set custom baudrate.",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        dest="timeout",
        type=int,
        default=5,
        help="Set the timeout for read and writes in seconds.",
    )
    parser.add_argument(
        "-r",
        "--raw",
        action="store_true",
        help="Display the data received from the board without any formatting (non-printable chars will be displayed in hex).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    # if no port was specified, try to pick one automatically
    port = args.port
    if port is None:
        port = find_device()
        if port is None:
            print(
                "Port not specified and could not detect a board automatically. Specify --port in arguments."
            )
            sys.exit(1)
        print(f"Found device: {port}. Specify -p argument to choose a different one.")
        print()

    # interface with device in basic read/write loop
    rc = RetCom87(
        port=port, baudrate=args.baudrate, timeout=args.timeout, show_raw=args.raw
    )
    rc.start_sequence()
    rc.simple_loop()
