# RetCom87-TerminalPython

Simple serial terminal written in Python for RetCom87.

## Dependencies
```
pip install -r requirements.txt
```
Note: I wrote this on Python 3.11. Haven't tested with other versions.

## Usage

Without any arguments, default configuration will be applied (see the help output for default values). It will try to find a valid serial port (name starting with `/dev/usbserial-...`) and connect to the first one it sees.

```
./rcterm.py
```

---

Example usage with port specified:

```
./rcterm.py -p /dev/cu.usbserial-A10LVXS7
```

Other cli options:

```
╰─ ./rcterm.py -h
usage: rcterm.py [-h] [-p PORT] [-b BAUDRATE] [-t TIMEOUT] [-r]

Basic serial interface for RetCom87

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Serial port of the board. If not specified, it will pick the first one it detects. (default: None)
  -b BAUDRATE, --baudrate BAUDRATE
                        Set custom baudrate. (default: 9600)
  -t TIMEOUT, --timeout TIMEOUT
                        Set the timeout for read and writes in seconds. (default: 5)
  -r, --raw             Display the data received from the board without any formatting (non-printable chars will be displayed in hex). (default: False)
```

#### Comparison of default vs raw (`-r`) output
Default output:

```
╰─ ./rcterm.py
Found device: /dev/cu.usbserial-A10LVXS7. Specify -p argument to choose a different one.

Using port: /dev/cu.usbserial-A10LVXS7
Baudrate: 9600
Press the reset button to begin.

==OUTPUT==

MENSCH ROM Version 2.07
(C) Copyright 1995
Assembled Mon Feb  6 10:03:42 1995

PCntr     Acc    Xreg   Yreg   Stack
00:E358   00 00  E0 B7  00 B3  01 FF

DirRg  F  DBk
00 00  22 00


Status Reg
N  V  M  X  D  I  Z  C
0  0  1  0  0  0  1  0

>
===

Command (hit enter to send):
```

Raw output:
```
╰─ ./rcterm.py -r
Found device: /dev/cu.usbserial-A10LVXS7. Specify -p argument to choose a different one.

Using port: /dev/cu.usbserial-A10LVXS7
Baudrate: 9600
Press the reset button to begin.

==RAW OUTPUT==
b'\x00\rMENSCH ROM Version 2.07\r (C) Copyright 1995\rAssembled Mon Feb  6 10:03:42 1995\r\rPCntr     Acc    Xreg   Yreg   Stack\r00:E358   00 00  E0 B7  00 B3  01 FF  \r\r  DirRg  F  DBk\r  00 00  22 00  \r\r\rStatus Reg\rN  V  M  X  D  I  Z  C\r0  0  1  0  0  0  1  0  \r\r>'
===

Command (hit enter to send):
```
This allows us to see the non-printable characters and also takes up less space.
