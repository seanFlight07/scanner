import scanning
import storage
import compare

def main():
    file_path = storage.file_path()
    file_name = storage.date_time_filename()
    network = "192.168.1.0/24"

    nmap_run = scanning.network_scan(network)
    #print(nmap_run)
    #storage.to_json(nmap_run, file_name, file_path)
    previous_scan = storage.load_json(file_path)
    compare.check_hosts(previous_scan, nmap_run)

if __name__=="__main__":
    main()
