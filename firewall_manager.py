# -----------------------------------------------
#  WINDOWS FIREWALL MANAGER
#  Cyber Security Internship - Task 4
#  Manage firewall rules through simple menu!
# -----------------------------------------------

import subprocess
import datetime
import os
import ctypes
import platform

# ---- PREDEFINED DANGEROUS PORTS ----------------
DANGEROUS_PORTS = {
    "23":   "Telnet - Sends data unencrypted",
    "21":   "FTP - File transfer unencrypted",
    "4444": "Metasploit - Common malware port",
    "5900": "VNC - Remote access risk",
    "1433": "SQL Server - Database exposure",
    "3389": "RDP - Remote desktop brute force",
    "8080": "HTTP Alternate - Often misconfigured"
}

SAFE_PORTS = {
    "80":  "HTTP - Web traffic",
    "443": "HTTPS - Secure web traffic",
    "22":  "SSH - Secure remote access",
    "53":  "DNS - Domain name resolution"
}

# ---- CHECK ADMIN -------------------------------
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# ---- BANNER ------------------------------------
def print_banner():
    os.system('cls')
    print("=" * 60)
    print("   WINDOWS FIREWALL MANAGER")
    print("   Cyber Security Internship - Task 4")
    print("   Date: " + str(datetime.datetime.now().strftime(
          "%Y-%m-%d %H:%M:%S")))
    print("   System: " + platform.node())
    print("=" * 60)
    if not is_admin():
        print()
        print("   WARNING: Run as Administrator for full access!")
    print()

# ---- MENU --------------------------------------
def print_menu():
    print("MAIN MENU:")
    print("-" * 40)
    print("  1 → List all active firewall rules")
    print("  2 → Block a port")
    print("  3 → Allow a port")
    print("  4 → Remove a firewall rule")
    print("  5 → Block all dangerous ports (auto)")
    print("  6 → Test if a port is open or blocked")
    print("  7 → View firewall status")
    print("  8 → Save current rules to file")
    print("  9 → Show dangerous ports list")
    print("  0 → Exit")
    print("-" * 40)

# ---- FUNCTIONS ---------------------------------

def list_rules():
    print()
    print("[*] Active Firewall Rules:")
    print("-" * 40)
    try:
        result = subprocess.run(
            ["powershell", "-Command",
             "Get-NetFirewallRule | "
             "Where-Object {$_.Enabled -eq 'True'} | "
             "Select-Object DisplayName, Direction, Action | "
             "Format-Table -AutoSize"],
            capture_output=True, text=True, timeout=30
        )
        print(result.stdout)
    except Exception as e:
        print("Error: " + str(e))

def block_port():
    print()
    port = input("Enter port number to BLOCK: ").strip()
    name = input("Enter rule name (e.g. Block_Telnet): ").strip()
    proto = input("Protocol TCP or UDP? (default TCP): ").strip()
    if proto.upper() not in ["TCP", "UDP"]:
        proto = "TCP"

    cmd = (
        'netsh advfirewall firewall add rule '
        'name="' + name + '" '
        'protocol=' + proto + ' '
        'dir=in localport=' + port + ' '
        'action=block'
    )
    print()
    print("[*] Running: " + cmd)
    result = subprocess.run(cmd, shell=True,
                           capture_output=True, text=True)
    if "Ok." in result.stdout:
        print("[OK] Port " + port + " BLOCKED successfully!")
        log_action("BLOCKED port " + port +
                  " (" + proto + ") - Rule: " + name)
    else:
        print("[ERROR] " + result.stdout + result.stderr)

def allow_port():
    print()
    port = input("Enter port number to ALLOW: ").strip()
    name = input("Enter rule name (e.g. Allow_HTTP): ").strip()
    proto = input("Protocol TCP or UDP? (default TCP): ").strip()
    if proto.upper() not in ["TCP", "UDP"]:
        proto = "TCP"

    cmd = (
        'netsh advfirewall firewall add rule '
        'name="' + name + '" '
        'protocol=' + proto + ' '
        'dir=in localport=' + port + ' '
        'action=allow'
    )
    print()
    print("[*] Running: " + cmd)
    result = subprocess.run(cmd, shell=True,
                           capture_output=True, text=True)
    if "Ok." in result.stdout:
        print("[OK] Port " + port + " ALLOWED successfully!")
        log_action("ALLOWED port " + port +
                  " (" + proto + ") - Rule: " + name)
    else:
        print("[ERROR] " + result.stdout + result.stderr)

def remove_rule():
    print()
    name = input("Enter exact rule name to REMOVE: ").strip()
    cmd = ('netsh advfirewall firewall delete rule '
           'name="' + name + '"')
    print()
    print("[*] Running: " + cmd)
    result = subprocess.run(cmd, shell=True,
                           capture_output=True, text=True)
    if "Ok." in result.stdout or "Deleted" in result.stdout:
        print("[OK] Rule '" + name + "' removed successfully!")
        log_action("REMOVED rule: " + name)
    else:
        print("[ERROR] Rule not found or could not be removed")
        print(result.stdout)

def block_all_dangerous():
    print()
    print("[*] Blocking all known dangerous ports...")
    print("-" * 40)
    blocked = []
    for port, desc in DANGEROUS_PORTS.items():
        name = "CyberTask4_Block_" + port
        cmd = (
            'netsh advfirewall firewall add rule '
            'name="' + name + '" '
            'protocol=TCP dir=in '
            'localport=' + port + ' action=block'
        )
        result = subprocess.run(cmd, shell=True,
                               capture_output=True, text=True)
        if "Ok." in result.stdout:
            print("[BLOCKED] Port " + port + " - " + desc)
            blocked.append(port)
            log_action("AUTO BLOCKED dangerous port " +
                      port + " - " + desc)
        else:
            print("[SKIP] Port " + port +
                  " - rule may already exist")

    print()
    print("[OK] Blocked " + str(len(blocked)) +
          " dangerous ports!")

def test_port():
    print()
    port = input("Enter port number to TEST: ").strip()
    print()
    print("[*] Testing port " + port + " on localhost...")
    try:
        result = subprocess.run(
            ["powershell", "-Command",
             "Test-NetConnection -ComputerName localhost "
             "-Port " + port + " -WarningAction SilentlyContinue"
             " | Select-Object RemotePort, TcpTestSucceeded"],
            capture_output=True, text=True, timeout=15
        )
        output = result.stdout.strip()
        print(output)
        if "True" in output:
            print()
            print("[RESULT] Port " + port +
                  " is OPEN (not blocked)")
        elif "False" in output:
            print()
            print("[RESULT] Port " + port +
                  " is CLOSED or BLOCKED")
        log_action("TESTED port " + port)
    except Exception as e:
        print("Error: " + str(e))

def firewall_status():
    print()
    print("[*] Windows Firewall Status:")
    print("-" * 40)
    try:
        result = subprocess.run(
            ["powershell", "-Command",
             "Get-NetFirewallProfile | "
             "Select-Object Name, Enabled, "
             "DefaultInboundAction, DefaultOutboundAction | "
             "Format-Table -AutoSize"],
            capture_output=True, text=True, timeout=15
        )
        print(result.stdout)
    except Exception as e:
        print("Error: " + str(e))

def save_rules():
    print()
    filename = "firewall_rules_" + \
               datetime.datetime.now().strftime(
               "%Y%m%d_%H%M%S") + ".txt"
    try:
        result = subprocess.run(
            ["powershell", "-Command",
             "Get-NetFirewallRule | "
             "Where-Object {$_.Enabled -eq 'True'} | "
             "Select-Object DisplayName, Direction, "
             "Action, Protocol | Format-Table -AutoSize"],
            capture_output=True, text=True, timeout=30
        )
        with open(filename, "w", encoding="utf-8") as f:
            f.write("WINDOWS FIREWALL RULES EXPORT\n")
            f.write("Date: " + str(datetime.datetime.now()) + "\n")
            f.write("System: " + platform.node() + "\n")
            f.write("=" * 60 + "\n\n")
            f.write(result.stdout)
        print("[OK] Rules saved to: " + filename)
        log_action("SAVED rules to " + filename)
    except Exception as e:
        print("Error: " + str(e))

def show_dangerous():
    print()
    print("DANGEROUS PORTS TO BLOCK:")
    print("-" * 40)
    for port, desc in DANGEROUS_PORTS.items():
        print("  Port " + port + " → " + desc)
    print()
    print("SAFE PORTS TO ALLOW:")
    print("-" * 40)
    for port, desc in SAFE_PORTS.items():
        print("  Port " + port + " → " + desc)

def log_action(action):
    with open("firewall_log.txt", "a",
              encoding="utf-8") as f:
        f.write("[" + str(datetime.datetime.now()) +
                "] " + action + "\n")

# ---- MAIN --------------------------------------
if __name__ == "__main__":
    while True:
        print_banner()
        print_menu()

        choice = input("Enter your choice: ").strip()
        print()

        if choice == "1":
            list_rules()
        elif choice == "2":
            block_port()
        elif choice == "3":
            allow_port()
        elif choice == "4":
            remove_rule()
        elif choice == "5":
            block_all_dangerous()
        elif choice == "6":
            test_port()
        elif choice == "7":
            firewall_status()
        elif choice == "8":
            save_rules()
        elif choice == "9":
            show_dangerous()
        elif choice == "0":
            print("[*] Exiting Firewall Manager. Goodbye!")
            break
        else:
            print("[!] Invalid choice! Try again.")

        print()
        input("Press Enter to continue...")
