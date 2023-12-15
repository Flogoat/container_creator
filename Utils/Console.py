from datetime import datetime
from colorama import Fore

class Console:
    @staticmethod
    def print_output(text: str):
        print(Fore.GREEN + "[OUTPUT] " + Fore.RESET + text)

    @staticmethod
    def print_info(text: str):
        print(Fore.BLUE + "[INFO] " + Fore.RESET + text)

    @staticmethod
    def print_error(text: str):
        print(Fore.RED + "[ERROR] " + Fore.RESET + text)

    @staticmethod
    def print_exec(text: str):
        print(Fore.CYAN + "[EXEC] " + Fore.RESET + text)

    @staticmethod
    def print_warning(text: str):
        print(Fore.YELLOW + "[WARNING] " + Fore.RESET + text)

    @staticmethod
    def print_time():
        print(f"[TIME] {datetime.now().strftime('%Y.%m.%d %H:%M:%S')}")

    @staticmethod
    def print_finished(text: str):
        print("\n" + Fore.MAGENTA + f"[FINISHED] {text}" + Fore.RESET)

    