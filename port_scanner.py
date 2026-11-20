import socket
import time

# Authorized scan targets
AUTHORIZED_TARGETS = ['127.0.0.1', 'scanme.nmap.org']

# Socket connection timeout in seconds
TIMEOUT = 1

# Delay between port scans in seconds
DELAY = 0.1

def validate_target(target):
    """Check whether the target is authorized for scanning."""
    if target not in AUTHORIZED_TARGETS:
        raise ValueError("Target is not authorized for scanning.")

    return target

def resolve_target(target):
    """Validate an authorized target and resolve it to an IP address."""
    validate_target(target)
    return socket.gethostbyname(target)

def validate_ports(start_port, end_port):
    """Check whether the port range is valid."""

    if type(start_port) is not int:
        raise ValueError("Starting port must be a whole number.")

    if type(end_port) is not int:
        raise ValueError("Ending port must be a whole number.")

    if not (1 <= start_port <= 65535):
        raise ValueError("Starting port must be between 1 and 65535.")
    
    if not (1 <= end_port <= 65535):
        raise ValueError("Ending port must be between 1 and 65535.")
    
    if start_port > end_port:
        raise ValueError("Start port cannot be greater than ending port.")

    return start_port, end_port

def scan_port(target_ip, port):
    """Check whether a specific TCP port is open or closed."""
    scanner = None

    try:
        scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        scanner.settimeout(TIMEOUT)
        
        scanner.connect((target_ip, port))
        return "open"

    except ConnectionRefusedError:
        return "closed"

    except socket.timeout:
        return "timed out"

    except OSError as error:
        return f"error: {error}"

    finally:
        if scanner is not None:
            scanner.close()

def scan_ports(target, start_port, end_port):
    """Scan a range of TCP ports on the target host."""
    target_ip = resolve_target(target)

    print(f"\nTarget: {target} ({target_ip})")

    open_ports = []
    closed_ports = []
    timed_out_ports = []

    print(f"Scanning {target} from port {start_port} to {end_port}...")

    start_time = time.monotonic()

    for port in range(start_port, end_port + 1):
        result = scan_port(target_ip, port)

        print(f"Port {port}: {result}")

        if result == "open":
            open_ports.append(port)
        elif result == "closed":
            closed_ports.append(port)
        elif result == "timed out":
            timed_out_ports.append(port)
            
        if port < end_port:
            time.sleep(DELAY)

    end_time = time.monotonic()
    
    scan_duration = end_time - start_time

    print("\nScan complete.")
    print(f"Open ports: {open_ports}")
    print(f"Closed ports: {closed_ports}")
    print(f"Timed out ports: {timed_out_ports}")
    print(f"Scan duration: {scan_duration:.2f} seconds.")

def main():
    """Get user input and run the port scanner."""
    try:
        target = input("Enter target (127.0.0.1 or scanme.nmap.org): ")

        start_port = int(input("Enter starting port: "))
        end_port = int(input("Enter ending port: "))

        validate_ports(start_port, end_port)

        scan_ports(target, start_port, end_port)

    except ValueError as error:
        print(f"Invalid input: {error}")

    except socket.gaierror:
        print("Unable to resolve target hostname.")

if __name__ == "__main__":
    main()

