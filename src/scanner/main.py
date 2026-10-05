import scanning
import storage
import compare
import report


def main():
    file_path = storage.file_path()
    file_name = storage.date_time_filename()
    network = "192.168.1.0/24"

    current_scan = scanning.network_scan(network)
    previous_scan = storage.load_json(file_path)

    added_hosts, removed_hosts, existing_hosts = compare.check_hosts(
        previous_scan,
        current_scan
    )

    port_changes = {}
    state_changes = {}

    for host in existing_hosts:
        added_ports, removed_ports, existing_ports = compare.check_ports(
            host,
            previous_scan,
            current_scan
        )

        if added_ports or removed_ports:
            port_changes[host] = {
                "added": added_ports,
                "removed": removed_ports
            }

        for port in existing_ports:
            state_change = compare.check_state(
                host,
                port,
                previous_scan,
                current_scan
            )

            if state_change:
                previous_state, current_state = state_change

                if host not in state_changes:
                    state_changes[host] = {}

                state_changes[host][port] = {
                    "previous": previous_state,
                    "current": current_state
                }

    scan_report = report.generate_report(
        added_hosts,
        removed_hosts,
        port_changes,
        state_changes
    )

    print(scan_report)

    report_file = report.save_report(scan_report)
    print(f"\nReport saved: {report_file}")

    
if __name__ == "__main__":
    main()