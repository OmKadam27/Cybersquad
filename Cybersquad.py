import os

def run_basic_scan():
    os.system('python Basic_scan.py')  

def run_complete_scan():
    os.system('python Complete_scan.py')  

def main():
    while True:
        print("**"*80)
        print("**"*80)
        print("\n")
        print("\n")
        print("                                                   CYBERSQUAD:Encouraging Security Investigators to Strengthen Systems                           ")
        print("\n")
        print("\n")
        print("**"*80)
        print("**"*80)
        print("\nSelect an option:")
        print("1) Basic Scan (Port scanning and directory scanning)")
        print("2) Complete Vulnerability Scanning")
        print("3) Exit")  

        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == '1':
            run_basic_scan()
        elif choice == '2':
            run_complete_scan()
        elif choice == '3':
            print("Exiting the program.")
            break  
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
