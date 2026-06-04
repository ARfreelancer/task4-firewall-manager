# Task 4 - Windows Firewall Manager

## Objective
Configure and test basic firewall rules to
allow or block network traffic on Windows.

## Tools Used
- Windows Firewall (netsh + PowerShell)
- Python 3 (custom firewall manager)

## Features of My Tool
| Feature | Description |
|---------|-------------|
| List Rules | Shows all active firewall rules |
| Block Port | Block any port with custom rule name |
| Allow Port | Allow any port through firewall |
| Remove Rule | Delete any firewall rule |
| Auto Block | Blocks all known dangerous ports |
| Test Port | Tests if port is open or blocked |
| Firewall Status | Shows all 3 profile statuses |
| Save Rules | Exports all rules to text file |

## How to Run
1. Open CMD as Administrator
2. cd C:\CyberTask4
3. python firewall_manager.py

## Ports Blocked During Task
| Port | Service | Reason |
|------|---------|--------|
| 23 | Telnet | Sends data unencrypted |
| 21 | FTP | Unencrypted file transfer |
| 4444 | Metasploit | Common malware port |
| 5900 | VNC | Remote access risk |
| 3389 | RDP | Brute force target |

## Key Concepts Learned
- What a firewall is and how it works
- Difference between stateful and stateless
- Inbound vs outbound rules
- How to block and allow ports on Windows
- Why certain ports are dangerous
