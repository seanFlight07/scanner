import json

def get_ports(host, scan):
    ports = scan["scan"][host].get("tcp", {})
    return ports


def check_ports(host, previous_scan, current_scan):
    current_ports = get_ports(host, current_scan)
    previous_ports = get_ports(host, previous_scan)
    
    current_ports = {int(port) for port in current_ports}
    previous_ports = {int(port) for port in previous_ports}

    added_ports = current_ports - previous_ports
    removed_ports = previous_ports - current_ports
    existing_ports = previous_ports & current_ports
    
    print(
        f"Added Ports: {added_ports} \n"
        f"Removed Ports: {removed_ports} \n"
        f"Existing Portss: {existing_ports}"
        )
    return added_ports, removed_ports, existing_ports

def check_hosts(previous_scan, current_scan):
    previous_hosts = set(previous_scan.get("scan"))
    current_hosts = set(current_scan.get("scan"))

    added_hosts = current_hosts - previous_hosts
    removed_hosts = previous_hosts - current_hosts
    existing_hosts = previous_hosts & current_hosts

    print(
        f"Added Hosts: {added_hosts} \n"
        f"Removed Hosts: {removed_hosts} \n"
        f"Existing Hosts: {existing_hosts}"
        )
    return added_hosts, removed_hosts, existing_hosts