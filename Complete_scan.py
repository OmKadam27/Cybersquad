import subprocess
import re
import matplotlib.pyplot as plt
import sys
import time
from collections import Counter

def loading_indicator():
    while loading[0]:
        for percentage in range(0, 101, 2): 
            sys.stdout.write(f"\rCybersquad: Working on your scan, please be patient... {percentage}%    ")
            sys.stdout.flush()
            time.sleep(0.2)  
        time.sleep(0.1)  

ip_address = input("Enter the IP address to scan: ")
loading = [True]

print("\nCybersquad: Working on your scan, please be patient...")
print(f"Working on the IP: {ip_address}")


import threading
loader_thread = threading.Thread(target=loading_indicator)
loader_thread.start()


command = f"nmap -sV --script vuln {ip_address}"
result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


loading[0] = False
loader_thread.join()

print("\n-----------------------------CYBERSCAN DATA-------------------------------------------------------\n")


output_lines = result.stdout.splitlines()
filtered_output = [line for line in output_lines if not any(phrase in line for phrase in [
    "Service detection performed.", 
    "Nmap done:",
    "Starting Nmap"  # Add this line to filter out the starting message
])]


for line in filtered_output:
    print(line)

if result.stderr:
    print("Errors:\n")
    print(result.stderr)


cpe_pattern = r"cpe:/\S+"
cpe_list = re.findall(cpe_pattern, result.stdout)

print("Extracted CPEs:", cpe_list)

if cpe_list:
    cpe_count = Counter(cpe_list)
    print("CPE Counts:", cpe_count)

    cpes = list(cpe_count.keys())
    counts = list(cpe_count.values())

    plt.figure(figsize=(10, 6))
    plt.barh(cpes, counts, color='steelblue')
    plt.xlabel('Number of Vulnerabilities')
    plt.ylabel('CPE')
    plt.title(f'CPE Vulnerability Analysis for {ip_address}')
    plt.tight_layout()
    plt.show()
else:
    print("No CPEs found in the CyberScan scan output.")

