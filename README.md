# Network Scanner

## Overview

Network Scanner is a personal cybersecurity and networking project designed to monitor devices and services on a local network and identify changes between scans.

I created this project while developing my understanding of networking, Linux, Python, Docker, and network security. Rather than simply running Nmap manually, I wanted to build a small monitoring system around it that could run automatically and maintain a history of the network over time.

The scanner runs an Nmap scan against the local network, stores the results as JSON, and compares each scan against the previous snapshot. Changes to hosts, ports, and port states are identified and written to a human-readable report.

The application is containerised with Docker and scheduled using a systemd timer, allowing the scanner to run automatically once per hour.

## Features

- Local network host discovery
- TCP port scanning using Nmap
- Detection of newly discovered hosts
- Detection of hosts that have disappeared from the network
- Detection of opened and removed ports
- Detection of changes to TCP port states
- JSON scan history
- Human-readable change reports
- Persistent scan and report storage
- Docker containerisation
- Host networking for local network discovery
- Automated hourly scans using systemd

## Architecture

The scanner uses a simple snapshot-based monitoring process.

```text
systemd timer
      │
      ▼
systemd service
      │
      ▼
Docker container
      │
      ▼
Python application
      │
      ├── Run Nmap scan
      │
      ├── Load previous JSON snapshot
      │
      ├── Compare hosts
      │      │
      │      └── Compare ports
      │             │
      │             └── Compare port states
      │
      ├── Generate report
      │
      └── Save current scan
              │
              ▼
       Persistent storage
```

Each execution is independent. The Docker container starts, performs the scan and comparison, saves the results, and then exits.

Persistent host directories are mounted into the container so scan history and reports remain available between container executions.

## How It Works

### 1. Network Scan

The application uses Nmap to scan the configured local network.

The results are collected through Python and used as the current network snapshot.

### 2. Load Previous Scan

Previous scan results are stored as timestamped JSON files.

Before performing the comparison, the application loads the most recent previous snapshot.

### 3. Compare Hosts

The scanner compares the hosts present in the previous and current scans.

Hosts are classified as:

- Added
- Removed
- Existing

Only hosts present in both snapshots require further comparison.

### 4. Compare Ports

For existing hosts, the TCP ports detected during each scan are compared.

Ports are classified as:

- Added
- Removed
- Existing

### 5. Compare Port States

Ports that exist in both scans are checked for state changes.

For example:

```text
22/tcp: open -> filtered
443/tcp: filtered -> open
```

This allows the scanner to detect changes without treating an existing port as newly discovered.

### 6. Generate Report

Detected changes are converted into a human-readable text report.

Example:

```text
HOST CHANGES
----------------------------------------
[+] 192.168.1.145
[-] 192.168.1.162

PORT CHANGES
----------------------------------------
192.168.1.20
    [+] 443/tcp
    [-] 80/tcp

STATE CHANGES
----------------------------------------
192.168.1.30
    22/tcp: filtered -> open
```

If no changes are detected, the report records that the network remained unchanged.

## Project Structure

```text
scanner/
├── src/
│   └── scanner/
│       ├── main.py
│       ├── scanning.py
│       ├── storage.py
│       ├── compare.py
│       └── report.py
│
├── data/
├── reports/
├── Dockerfile
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

### `main.py`

Coordinates the complete scanning workflow.

### `scanning.py`

Handles communication with Nmap and performs the network scan.

### `storage.py`

Handles JSON persistence, timestamped filenames, and loading previous scan results.

### `compare.py`

Contains the comparison logic for hosts, ports, and port states.

### `report.py`

Converts detected changes into a readable report and saves the report to disk.

## Docker

The application is packaged as a Docker image.

Build the image from the repository root:

```bash
sudo docker build -t network-scanner .
```

Run the scanner manually:

```bash
sudo docker run --rm \
  --network host \
  -v /etc/localtime:/etc/localtime:ro \
  -v /etc/timezone:/etc/timezone:ro \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/reports:/app/reports" \
  network-scanner
```

### Host Networking

The scanner uses:

```text
--network host
```

This gives the container access to the host's network stack, allowing Nmap to inspect devices on the local network.

This deployment method is intended for Linux hosts.

### Persistent Storage

Two host directories are mounted into the container:

```text
./data     -> /app/data
./reports  -> /app/reports
```

The container itself is disposable.

When a scan finishes, the container exits and is removed, while the JSON snapshots and reports remain on the host.

## Automated Scanning

The deployed scanner uses a systemd oneshot service.

Example:

```ini
[Unit]
Description=Network Scanner Docker Container
Requires=docker.service
After=docker.service network-online.target

[Service]
Type=oneshot
WorkingDirectory=/path/to/scanner

ExecStart=/usr/bin/docker run --rm \
    --network host \
    -v /etc/localtime:/etc/localtime:ro \
    -v /etc/timezone:/etc/timezone:ro \
    -v /path/to/scanner/data:/app/data \
    -v /path/to/scanner/reports:/app/reports \
    network-scanner
```

A systemd timer triggers the service once per hour:

```ini
[Unit]
Description=Run Network Scanner Hourly

[Timer]
OnBootSec=5min
OnUnitActiveSec=1h
Persistent=true

[Install]
WantedBy=timers.target
```

Enable the timer with:

```bash
sudo systemctl enable --now network-scanner.timer
```

The timer can be checked using:

```bash
systemctl list-timers --all | grep network-scanner
```

This provides the following deployment lifecycle:

```text
Timer triggers
      ↓
Container starts
      ↓
Network scanned
      ↓
Changes detected
      ↓
Report generated
      ↓
Snapshot saved
      ↓
Container exits
      ↓
Wait for next scheduled run
```

## Data and Privacy

Network scan results are deliberately excluded from the repository.

The following directories are ignored by Git:

```text
data/
reports/
```

These files can contain information about devices, IP addresses, and services running on the local network and should not be committed to a public repository.

## Technologies

- Python
- Nmap
- python-nmap
- Docker
- Linux
- systemd
- JSON

## What I Learned

This project gave me practical experience with several areas of networking and software development, including:

- Network discovery and TCP port scanning
- Understanding Nmap scan results
- Working with changing network state
- Comparing structured data between snapshots
- JSON persistence
- Python file and path handling
- Separating an application into focused modules
- Docker image creation
- Docker networking and persistent volumes
- Linux services
- systemd timers
- Automated background workloads

One of the more interesting challenges was handling differences between live Nmap results and JSON data. JSON object keys are stored as strings, while port numbers returned by the live scanner can be integers. Normalising these values before comparison prevents unchanged ports from incorrectly appearing as both added and removed.

## Future Improvements

The current version intentionally focuses on providing a small and reliable network monitoring tool.

Potential future improvements include:

- Configurable network ranges
- More detailed service information
- OS detection
- Improved Nmap scan profiles
- Device identification
- Historical change tracking
- Structured logging
- Alerting when unexpected devices or services appear
- Database-backed scan history
- Web-based monitoring dashboard
- Deployment to a dedicated Raspberry Pi or homelab environment

## Status

**Version 1.0**

The initial version provides automated local network scanning, snapshot comparison, change reporting, Docker deployment, persistent storage, and hourly execution using systemd.