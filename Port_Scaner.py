import socket
import threading
import time
import argparse
from concurrent.futures import ThreadPoolExecutor

lock = threading.Lock()
open_ports = []


def scan_port(target_ip, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target_ip, port))
            if result == 0:
                service = ""
                try:
                    service = socket.getservbyport(port, "tcp")
                except:
                    pass

                with lock:
                    open_ports.append((port, service))
    except:
        pass


def parse_ports(port_range):
    try:
        start, end = map(int, port_range.split("-"))
        if start < 0 or end > 65535 or start > end:
            raise ValueError
        return start, end
    except:
        raise argparse.ArgumentTypeError("Port range must be like 1-1000")


def main():
    parser = argparse.ArgumentParser(description="Simple TCP Port Scanner")
    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("-p", "--ports", required=True,
                        help="Port range (example 1-1000)")
    parser.add_argument("-t", "--threads", type=int, default=200,
                        help="Number of threads (default 200)")
    parser.add_argument("--timeout", type=float, default=1,
                        help="Socket timeout in seconds (default 1)")
    parser.add_argument("-o", "--output", help="Save results to file")

    args = parser.parse_args()

    start_time = time.time()

    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print("Could not resolve hostname.")
        return

    start_port, end_port = parse_ports(args.ports)

    print(f"\nScanning {args.target} ({target_ip})")
    print(f"Ports: {start_port}-{end_port}")
    print(f"Threads: {args.threads}\n")

    max_threads = min(args.threads, end_port - start_port + 1)

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, target_ip, port, args.timeout)

    results = sorted(open_ports)

    for port, service in results:
        if service:
            print(f"[OPEN] {port}/tcp ({service})")
        else:
            print(f"[OPEN] {port}/tcp")

    if args.output:
        with open(args.output, "w") as f:
            for port, service in results:
                if service:
                    f.write(f"{port}/tcp ({service})\n")
                else:
                    f.write(f"{port}/tcp\n")

    end_time = time.time()
    print(f"\nScan completed in {end_time - start_time:.2f} seconds")
    print(f"Total open ports: {len(results)}")


if __name__ == "__main__":
    main()
