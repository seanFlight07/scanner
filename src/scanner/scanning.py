import json
import nmap
from datetime import datetime
from pathlib import Path

scanner = nmap.PortScanner()

network = "192.168.1.0/24"

def network_scan(network):
    scanner.scan(
        hosts=network,
        arguments="-sn"
    )

    active_networks = []

    for host in scanner.all_hosts():
        if scanner[host].state() == "up":
            active_networks.append(host)

    active_hosts = " ".join(active_networks)

    scan_log = scanner.scan(
        hosts=active_hosts,
        arguments="--top-ports 10"
    )

    return scan_log

def to_json(log, file_name):
    json_log = json.dumps(log)
    data_dir = Path(__file__).resolve().parents[2] / "data"
    with open(data_dir /file_name, "w") as f:
        f.write(json_log)

def date_time():
    current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M")
    str_datetime = str(current_datetime)
    file_name = str_datetime + ".json"
    return file_name









log = network_scan(network)
file = date_time()
test = to_json(log, file)

for ip, host_data in log["scan"].items():

    print(f"\nHost: {ip}")

    for port, port_data in host_data["tcp"].items():
        print(port, port_data["state"], port_data["name"])


