import scanning
import storage
import compare

def main():
    file_path = storage.file_path()
    file_name = storage.date_time_filename()
    network = "192.168.1.0/24"

    current_scan = scanning.network_scan(network)
    previous_scan = storage.load_json(file_path)
    added_hosts, removed_hosts, existing_hosts = compare.check_hosts(previous_scan, current_scan)

    for host in added_hosts:
        #print("Added host ports"+ host)
        ports =compare.get_ports(host, current_scan)
       # print(ports)

    for host in existing_hosts:
        added_ports, removed_ports, existing_ports = compare.check_ports(
        host,
        previous_scan,
        current_scan
    )

        for port in existing_ports:
            compare.check_state(
                host,
                port,
                previous_scan,
                current_scan
            )

if __name__=="__main__":
    main()
