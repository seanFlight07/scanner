import json

def check_hosts(previous_scan, current_scan):
    previous_hosts = set(previous_scan.get("scan"))
    current_hosts = set(current_scan.get("scan"))

    print(previous_hosts)
    print(current_hosts)

    added_hosts = current_hosts - previous_hosts
    removed_hosts = previous_hosts - current_hosts
    existing_hosts = previous_hosts & current_hosts

    print(
        f"Added Hosts: {added_hosts} \n"
        f"Removed Hosts: {removed_hosts} \n"
        f"Existing Hosts: {existing_hosts}"
        )
