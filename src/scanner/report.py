def print_hosts(added_hosts, removed_hosts):
    print("HOST CHANGES")
    print("-" * 40)

    if added_hosts:
        for host in sorted(added_hosts):
            print(f"[+] {host}")

    if removed_hosts:
        for host in sorted(removed_hosts):
            print(f"[-] {host}")

    if not added_hosts and not removed_hosts:
        print("No host changes detected.")

    print()


def print_ports(port_changes):
    print("PORT CHANGES")
    print("-" * 40)

    if not port_changes:
        print("No port changes detected.")
        print()
        return

    for host, changes in port_changes.items():
        print(host)

        for port in sorted(changes["added"]):
            print(f"    [+] {port}/tcp")

        for port in sorted(changes["removed"]):
            print(f"    [-] {port}/tcp")

        print()

def print_states(state_changes):
    print("STATE CHANGES")
    print("-" * 40)

    if not state_changes:
        print("No state changes detected.")
        print()
        return

    for host, ports in state_changes.items():
        print(host)

        for port, states in sorted(ports.items()):
            print(
                f"    {port}/tcp: "
                f"{states['previous']} -> {states['current']}"
            )

        print()