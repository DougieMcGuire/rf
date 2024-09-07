import os
import time
import subprocess

# Define the ASCII art for credits and edit path
ascii_art = [
    " ██▀███   ▄▄▄       ██▓ ███▄    █   █████▒▄▄▄       ██▓     ██▓    ",
    "▓██ ▒ ██▒▒████▄    ▓██▒ ██ ▀█   █ ▓██   ▒▒████▄    ▓██▒    ▓██▒    ",
    "▓██ ░▄█ ▒▒██  ▀█▄  ▒██▒▓██  ▀█ ██▒▒████ ░▒██  ▀█▄  ▒██░    ▒██░    ",
    "▒██▀▀█▄  ░██▄▄▄▄██ ░██░▓██▒  ▐▌██▒░▓█▒  ░░██▄▄▄▄██ ▒██░    ▒██░    ",
    "░██▓ ▒██▒ ▓█   ▓██▒░██░▒██░   ▓██░░▒█░    ▓█   ▓██▒░██████▒░██████▒",
    "░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░▓  ░ ▒░   ▒ ▒  ▒ ░    ▒▒   ▓▒█░░ ▒░▓  ░░ ▒░▓  ░",
    "  ░▒ ░ ▒░  ▒   ▒▒ ░ ▒ ░░ ░░   ░ ▒░ ░       ▒   ▒▒ ░░ ░ ▒  ░░ ░ ▒  ░",
    "  ░░   ░   ░   ▒    ▒ ░   ░   ░ ░  ░ ░     ░   ▒     ░ ░     ░ ░   ",
    "   ░           ░  ░ ░           ░              ░  ░    ░  ░    ░  ░",
    "                                                                   "
]
ascii_art_credits = [
    " ▄████▄   ██▀███  ▓█████ ▓█████▄  ██▓▄▄▄█████▓  ██████ ",
    "▒██▀ ▀█  ▓██ ▒ ██▒▓█   ▀ ▒██▀ ██▌▓██▒▓  ██▒ ▓▒▒██    ▒ ",
    "▒▓█    ▄ ▓██ ░▄█ ▒▒███   ░██   █▌▒██▒▒ ▓██░ ▒░░ ▓██▄   ",
    "▒▓▓▄ ▄██▒▒██▀▀█▄  ▒▓█  ▄ ░▓█▄   ▌░██░░ ▓██▓ ░   ▒   ██▒",
    "▒ ▓███▀ ░░██▓ ▒██▒░▒████▒░▒████▓ ░██░  ▒██▒ ░ ▒██████▒▒",
    "░ ░▒ ▒  ░░ ▒▓ ░▒▓░░░ ▒░ ░ ▒▒▓  ▒ ░▓    ▒ ░░   ▒ ▒▓▒ ▒ ░",
    "  ░  ▒     ░▒ ░ ▒░ ░ ░  ░ ░ ▒  ▒  ▒ ░    ░    ░ ░▒  ░ ░",
    "░          ░░   ░    ░    ░ ░  ░  ▒ ░  ░      ░  ░  ░  ",
    "░ ░         ░        ░  ░   ░     ░                 ░  ",
    "░                         ░                            "
]

ascii_art_info = [
    "╔═══════════════════════════════╦═══════════════════════════════════════════════════════════════════╗",
    "║ 	                        ║	                        	                            ║",
    "║ 	    ▄██████▄	        ║	██████   ██████   ██      ██  ██████   ██  ███████          ║",
    "║ 	    ████████	        ║	██   ██ ██     ██ ██      ██ ██            ██               ║",
    "║ 	    ████████            ║	██   ██ ██     ██ ██      ██ ██   ███  ██  █████            ║",
    "║ 	  ▀▀████████▀▀		║	██   ██ ██     ██   ██  ██   ██    ██  ██  ██               ║",
    "║ 	    ████████ 		║	██   ██ ██     ██   ██  ██   ██    ██  ██  ██               ║",
    "║ 	  █▄████████▄█		║	██████   ██████      ████     ██████   ██  ███████          ║",
    "║ 	   ▀▀█▀██▀█▀▀		║	                        	                            ║",
    "║ 	                        ║	                        	                            ║",
    "╠═══════════════════════════════╬═══════════════════════════════════════════════════════════════════╣",
    "║	                        ║	                        	                            ║",
    "║  	    ▄██████▄		║	                        	                            ║",
    "║ 	    ████████	        ║ 	 ███████  ███████   ██   ██    ██████   ███████  ███████    ║",
    "║ 	    ████████	        ║ 	██       ██          ██ ██    ██    ██ ██       ██          ║",
    "║ 	  ▀▀████████▀▀		║	 ███████  ███████     ███     ██    ██ ███████   ███████    ║",
    "║  	    ████████ 		║	       ██       ██   ██ ██    ██    ██       ██        ██   ║",
    "║	  █▄████████▄█		║	 ███████  ███████   ██   ██    ██████  ███████   ███████    ║",
    "║	   ▀▀█▀██▀█▀▀		║	                        	                            ║",
    "║ 	                        ║	                        	                            ║",
    "╚═══════════════════════════════╩═══════════════════════════════════════════════════════════════════╝",

]

path_art = [
    "██████   █████  ███████ ████████ ███████     ██████   █████  ████████ ██   ██ ",
    "██   ██ ██   ██ ██         ██    ██          ██   ██ ██   ██    ██    ██   ██ ",
    "██████  ███████ ███████    ██    █████       ██████  ███████    ██    ███████ ",
    "██      ██   ██      ██    ██    ██          ██      ██   ██    ██    ██   ██ ",
    "██      ██   ██ ███████    ██    ███████     ██      ██   ██    ██    ██   ██ ",
    "                                                                             "
]

# Function to print ASCII art line by line with a delay
def print_ascii_art_line_by_line(ascii_art, delay=0.05):
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal screen
    for row in ascii_art:
        print(row)
        time.sleep(delay)  # Delay between lines
    print("\n")  # Add some space after the ASCII art

def print_credits():
    print_ascii_art_line_by_line(ascii_art_credits)
    time.sleep(2)  # Wait for 2 seconds
    print_ascii_art_line_by_line(ascii_art_info)

def print_menu():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal screen
    print_ascii_art_line_by_line(ascii_art)
    print("1. Start")
    print("2. Credits")
    print("3. Edit Path To ChromeDriver")
    print("4. Download Requirements")
    choice = input("Please select an option (1-4): ")
    return choice

def main():
    while True:
        choice = print_menu()
        
        if choice == "1":
            # Execute o.py script
            os.system("python scripts/o.py")
        elif choice == "2":
            # Print credits ASCII art
            print_credits()
            input("More: https://dougie.wtf/ Press Enter to continue...")
        elif choice == "3":
            # Edit path to ChromeDriver
            print_ascii_art_line_by_line(path_art)
            new_path = input("Enter the new path for ChromeDriver: ")
            with open("scripts/path.txt", "w") as f:
                f.write(new_path)
            print("Saved!")
        elif choice == "4":
            # Download requirements
            install = input("Would you like to install Requirements.TXT? Y/N: ").strip().upper()
            if install == "Y":
                subprocess.call(["pip", "install", "-r", "scripts/requirements.txt"])
            else:
                print("Skipping requirement installation.")
        else:
            print("Invalid option. Please try again.")
        
        # Prompt to continue or exit
        continue_choice = input("Do you want to return to the main menu? (yes/no): ").strip().lower()
        if continue_choice != "yes":
            break

if __name__ == "__main__":
    main()
