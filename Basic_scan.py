import subprocess
from datetime import datetime

IMPORTANT_DIRECTORIES = [
    "admin",
    "login",
    "config",
    "phpMyAdmin",
    "wp-admin",
    "dashboard",
    "cgi-bin",
    "uploads",
    "backup",
    "test",
    "twiki",
]

def run_dirb(ip_address, wordlist=None, protocol="http"):
    target_url = f"{protocol}://{ip_address}"
    start_time = datetime.now().strftime("%a %b %d %H:%M:%S %Y")
    
    report_filename = f"dirb_report_{ip_address.replace('.', '_')}.txt"
    
    with open(report_filename, 'w') as report_file:
        report_file.write(f"START_TIME: {start_time}\n")
        report_file.write(f"URL_BASE: {target_url}\n")
        if wordlist:
            report_file.write(f"WORDLIST_FILES: {wordlist}\n\n")

        command = ['dirb', target_url]
        if wordlist:
            command.append(wordlist)

        try:  
            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0:
                lines = result.stdout.splitlines()
                
                cleaned_output = [
                    line for line in lines 
                    if line.strip() and "Calculating NOT_FOUND code..." not in line
                ]

                important_results = [
                    line for line in cleaned_output 
                    if any(important_dir in line for important_dir in IMPORTANT_DIRECTORIES)
                ]

                generated_words = len(cleaned_output)
                report_file.write(f"GENERATED WORDS: {generated_words}\n")
                report_file.write(f"\n---- Scanning URL: {target_url} ----\n")
                
                if important_results:
                    report_file.write("\n".join(important_results) + "\n")
                else:
                    report_file.write("No important directories found.\n")

            else:
                report_file.write("Dirb Scan Failed:\n")
                report_file.write(result.stderr + "\n")

        except Exception as e:
            report_file.write(f"Error running dirb: {e}\n")

        end_time = datetime.now().strftime("%a %b %d %H:%M:%S %Y")
        report_file.write(f"\n-----------------\nEND_TIME: {end_time}\n")
        report_file.write(f"DOWNLOADED: 18448 - FOUND: {len(important_results)}\n")

    print(f"Report generated: {report_filename}")


def run_nmap_scan(ip_address):
    try:
        n_command = ['nmap', ip_address]
        result = subprocess.run(n_command, capture_output=True, text=True)

        if result.returncode == 0:
            return result.stdout
        else:
            return f"Uff We Failed To Scan Failed:\n{result.stderr}"
    except Exception as e:
        return f"Error running Nmap: {e}"

if __name__ == "__main__":
    ip_address = input("Enter the target IP address (e.g., 192.168.1.1): ")

    protocol = input("Enter the protocol (http or https): ").strip().lower()
    if protocol not in ['http', 'https']:
        protocol = 'http'

    use_wordlist = input("Do you want to specify a custom wordlist? (y/n): ").strip().lower()
    wordlist = None
    if use_wordlist == 'y':
        wordlist = input("Enter the full path to your wordlist file: ")

    print("\n---- Running Port Scan ----------")
    results = run_nmap_scan(ip_address)
    print(results)

    run_dirb(ip_address, wordlist, protocol)

    with open(f"dirb_report_{ip_address.replace('.', '_')}.txt", 'a') as report_file:
        report_file.write("\n--- CYBERSQUAD BASIC Scan Results ---\n")
        report_file.write(results)
