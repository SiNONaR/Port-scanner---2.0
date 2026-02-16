# TCP Port Scanner

A simple and fast TCP port scanner written in Python.
This tool allows scanning a range of ports on a target IP or hostname and supports saving the results to a file.

---

## Features

- Scan a range of TCP ports
- Multi-threaded scanning for faster results
- Detects common services (http, ssh, ftp, etc.)
- Save results to a file
- CLI tool using `argparse`

---

## Usage

```bash
python Port_Scaner.py <target> -p 1-1000 -t 200 -o results.txt
