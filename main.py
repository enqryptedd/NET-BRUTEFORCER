import argparse
from Bruteforcer import Bruteforcer
from colorama import init, Fore, Style
import threading

init()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", help="Interface to use for scanning", required=True)
    parser.add_argument("-w", "--wordlist", help="Path to the wordlist file", required=True)
    args = parser.parse_args()
    print(f"""
{Fore.GREEN}███    ██ ███████ ████████     ██████  ██████  ██    ██ ████████ ███████ ███████  ██████  ██████   ██████ ███████ {Style.RESET_ALL}
{Fore.GREEN}████   ██ ██         ██        ██   ██ ██   ██ ██    ██    ██    ██      ██      ██    ██ ██   ██ ██      ██      {Style.RESET_ALL}
{Fore.GREEN}██ ██  ██ █████      ██        ██████  ██████  ██    ██    ██    █████   █████   ██    ██ ██████  ██      █████   {Style.RESET_ALL}
{Fore.GREEN}██  ██ ██ ██         ██        ██   ██ ██   ██ ██    ██    ██    ██      ██      ██    ██ ██   ██ ██      ██      {Style.RESET_ALL}
{Fore.GREEN}██   ████ ███████    ██        ██████  ██   ██  ██████     ██    ███████ ██       ██████  ██   ██  ██████ ███████ {Style.RESET_ALL}
{Fore.CYAN}
            WiFi Brute Forcer
            ------------------
{Style.RESET_ALL}
""")
    bruteforcer = Bruteforcer(args.interface, args.wordlist)
    bruteforcer.start()

if __name__ == "__main__":
    main()