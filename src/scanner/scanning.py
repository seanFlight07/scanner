import nmap

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

