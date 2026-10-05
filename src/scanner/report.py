from pathlib import Path
from datetime import datetime

def hosts_report(added_hosts, removed_hosts):
    lines = [
        "HOST CHANGES",
        "-" * 40
    ]

    if added_hosts:
        for host in sorted(added_hosts):
            lines.append(f"[+] {host}")

    if removed_hosts:
        for host in sorted(removed_hosts):
            lines.append(f"[-] {host}")

    if not added_hosts and not removed_hosts:
        lines.append("No host changes detected.")

    return "\n".join(lines)


def ports_report(port_changes):
    lines = [
        "PORT CHANGES",
        "-" * 40
    ]

    if not port_changes:
        lines.append("No port changes detected.")
        return "\n".join(lines)

    for host, changes in port_changes.items():
        lines.append(host)

        for port in sorted(changes["added"]):
            lines.append(f"    [+] {port}/tcp")

        for port in sorted(changes["removed"]):
            lines.append(f"    [-] {port}/tcp")

    return "\n".join(lines)

def states_report(state_changes):
    lines = [
        "STATE CHANGES",
        "-" * 40
    ]

    if not state_changes:
        lines.append("No state changes detected.")
        return "\n".join(lines)

    for host, ports in state_changes.items():
        lines.append(host)

        for port, states in sorted(ports.items()):
            lines.append(
                f"    {port}/tcp: "
                f"{states['previous']} -> {states['current']}"
            )

    return "\n".join(lines)

def generate_report(
    added_hosts,
    removed_hosts,
    port_changes,
    state_changes
):
    sections = [
        hosts_report(added_hosts, removed_hosts),
        ports_report(port_changes),
        states_report(state_changes)
    ]

    return "\n\n".join(sections)

def save_report(scan_report):
    report_path = Path(__file__).resolve().parents[2] / "reports"
    report_path.mkdir(parents=True, exist_ok=True)

    file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.txt")
    file_path = report_path / file_name

    with open(file_path, "w") as file:
        file.write(scan_report)

    return file_path