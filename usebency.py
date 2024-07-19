import os
import sys
import shutil
import json
import logging
import base64
import getpass
import time
from typing import Dict, Any
from colorama import Fore, Style, init
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

init(autoreset=True)

class USEBENCYManager:
    def __init__(self):
        self.banner = '''
█    ██   ██████ ▓█████  ▄▄▄▄   ▓█████  ███▄    █  ▄████▄▓██   ██▓
 ██  ▓██▒▒██    ▒ ▓█   ▀ ▓█████▄ ▓█   ▀  ██ ▀█   █ ▒██▀ ▀█ ▒██  ██▒
▓██  ▒██░░ ▓██▄   ▒███   ▒██▒ ▄██▒███   ▓██  ▀█ ██▒▒▓█    ▄ ▒██ ██░
▓▓█  ░██░  ▒   ██▒▒▓█  ▄ ▒██░█▀  ▒▓█  ▄ ▓██▒  ▐▌██▒▒▓▓▄ ▄██▒░ ▐██▓░
▒▒█████▓ ▒██████▒▒░▒████▒░▓█  ▀█▓░▒████▒▒██░   ▓██░▒ ▓███▀ ░░ ██▒▓░
░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░░░ ▒░ ░░▒▓███▀▒░░ ▒░ ░░ ▒░   ▒ ▒ ░ ░▒ ▒  ░ ██▒▒▒ 
░░▒░ ░ ░ ░ ░▒  ░ ░ ░ ░  ░▒░▒   ░  ░ ░  ░░ ░░   ░ ▒░  ░  ▒  ▓██ ░▒░ 
 ░░░ ░ ░ ░  ░  ░     ░    ░    ░    ░      ░   ░ ░ ░       ▒ ▒ ░░  
   ░           ░     ░  ░ ░         ░  ░         ░ ░ ░     ░ ░     
                               ░                   ░       ░ ░     
'''
        self.drives_file = 'usebency_drives.json'
        self.drives: Dict[str, Dict[str, str]] = {}
        self.terminal_width = shutil.get_terminal_size().columns
        self.load_drives()
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(filename='usebency.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def center_text(self, text: str) -> str:
        return text.center(self.terminal_width)

    def print_centered(self, text: str, color: str = Fore.WHITE):
        print(color + self.center_text(text) + Style.RESET_ALL)

    def print_banner(self):
        for line in self.banner.split('\n'):
            self.print_centered(line, Fore.RED)
        self.print_centered("Gestion sécurisée de vos clés USB - v2.0", Fore.CYAN)
        self.print_centered("=" * 45, Fore.YELLOW)

    def print_menu(self, title: str, options: list):
        self.clear_screen()
        self.print_banner()
        print()
        self.print_centered(title, Fore.CYAN + Style.BRIGHT)
        self.print_centered("=" * (len(title) + 4), Fore.YELLOW)
        for i, option in enumerate(options, 1):
            self.print_centered(f"{i}. {option}", Fore.GREEN)
        self.print_centered("=" * (len(title) + 4), Fore.YELLOW)

    def get_user_input(self, prompt: str) -> str:
        return input(prompt)

    def get_password(self, prompt: str) -> str:
        return getpass.getpass(prompt)

    def get_user_choice(self, max_choice: int) -> int:
        while True:
            try:
                choice = int(self.get_user_input(f"Choisissez une option (1-{max_choice}): "))
                if 1 <= choice <= max_choice:
                    return choice
                else:
                    self.print_centered(f"Choix invalide. Veuillez entrer un nombre entre 1 et {max_choice}.", Fore.RED)
            except ValueError:
                self.print_centered("Entrée invalide. Veuillez entrer un nombre.", Fore.RED)

    def load_drives(self):
        try:
            if os.path.exists(self.drives_file):
                with open(self.drives_file, 'r') as f:
                    self.drives = json.load(f)
            logging.info("Drives loaded successfully")
        except Exception as e:
            logging.error(f"Error loading drives: {str(e)}")
            self.print_centered("Erreur lors du chargement des informations des lecteurs.", Fore.RED)

    def save_drives(self):
        try:
            with open(self.drives_file, 'w') as f:
                json.dump(self.drives, f)
            logging.info("Drives saved successfully")
        except Exception as e:
            logging.error(f"Error saving drives: {str(e)}")
            self.print_centered("Erreur lors de la sauvegarde des informations des lecteurs.", Fore.RED)

    def generate_key(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def encrypt_file(self, file_path: str, key: bytes):
        f = Fernet(key)
        with open(file_path, 'rb') as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        with open(file_path, 'wb') as file:
            file.write(encrypted_data)

    def decrypt_file(self, file_path: str, key: bytes):
        f = Fernet(key)
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = f.decrypt(encrypted_data)
        with open(file_path, 'wb') as file:
            file.write(decrypted_data)

    def show_animation(self):
        frames = [
            "F", "Fa", "Fai", "Fait", "Fait ", "Fait p", "Fait pa", "Fait par",
            "Fait par ", "Fait par T", "Fait par Ti", "Fait par Tit",
            "Fait par Tito", "Fait par Titou", "Fait par Titoua",
            "Fait par Titouan", "Fait par Titouan ", "Fait par Titouan C",
            "Fait par Titouan Co", "Fait par Titouan Cor", "Fait par Titouan Corn",
            "Fait par Titouan Corni", "Fait par Titouan Cornil",
            "Fait par Titouan Cornill", "Fait par Titouan Cornille",
        ]
        for frame in frames:
            self.clear_screen()
            print("\n" * 10)
            self.print_centered(frame, Fore.CYAN)
            time.sleep(0.1)
            
        time.sleep(1)
        self.clear_screen()
        self.print_banner()
        time.sleep(4)

    def calculate_size_difference(self, drive_letter: str) -> float:
        total_size_before = 0
        total_size_after = 0

        for root, dirs, files in os.walk(f"{drive_letter}:\\"):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                total_size_before += file_size
                total_size_after += ((file_size + 16) // 16 + 1) * 16  # Fernet adds at most 16 bytes per block

        size_difference_gb = (total_size_after - total_size_before) / (1024 * 1024 * 1024)
        return size_difference_gb

    def encrypt_drive(self):
        self.clear_screen()
        self.print_banner()
        self.print_centered("Chiffrement d'une clé USB", Fore.CYAN)
        
        drive_letter = self.get_user_input("Entrez la lettre du lecteur de la clé USB (ex: E): ")
        
        if not os.path.exists(f"{drive_letter}:\\"):
            self.print_centered(f"Le lecteur {drive_letter}: n'existe pas.", Fore.RED)
            self.get_user_input("Appuyez sur Entrée pour continuer...")
            return

        password = self.get_password("Entrez un mot de passe pour le chiffrement : ")
        confirm_password = self.get_password("Confirmez le mot de passe : ")

        if password != confirm_password:
            self.print_centered("Les mots de passe ne correspondent pas.", Fore.RED)
            self.get_user_input("Appuyez sur Entrée pour continuer...")
            return

        self.print_centered("Calcul de l'espace supplémentaire nécessaire...", Fore.YELLOW)
        size_difference = self.calculate_size_difference(drive_letter)
        self.print_centered(f"Le chiffrement ajoutera environ {size_difference:.2f} Go.", Fore.YELLOW)
        self.print_centered(f"Mot de passe choisi : {password}", Fore.YELLOW)
        
        confirm = self.get_user_input("Voulez-vous continuer ? (o/n): ")
        if confirm.lower() != 'o':
            self.print_centered("Opération annulée.", Fore.RED)
            self.get_user_input("Appuyez sur Entrée pour continuer...")
            return

        salt = os.urandom(16)
        key = self.generate_key(password, salt)

        self.print_centered("Chiffrement en cours...", Fore.YELLOW)

        try:
            for root, dirs, files in os.walk(f"{drive_letter}:\\"):
                for file in files:
                    file_path = os.path.join(root, file)
                    self.encrypt_file(file_path, key)

            self.drives[drive_letter] = {
                "salt": base64.b64encode(salt).decode(),
                "is_encrypted": True
            }
            self.save_drives()

            self.print_centered("Clé USB chiffrée avec succès !", Fore.GREEN)
            logging.info(f"Drive {drive_letter}: encrypted successfully")
        except Exception as e:
            self.print_centered(f"Une erreur s'est produite lors du chiffrement : {str(e)}", Fore.RED)
            logging.error(f"Error encrypting drive {drive_letter}: {str(e)}")

        self.get_user_input("Appuyez sur Entrée pour continuer...")

    def decrypt_drive(self):
        self.clear_screen()
        self.print_banner()
        self.print_centered("Déchiffrement d'une clé USB", Fore.CYAN)
        
        drive_letter = self.get_user_input("Entrez la lettre du lecteur de la clé USB (ex: E): ")
        
        if drive_letter not in self.drives or not self.drives[drive_letter].get("is_encrypted", False):
            self.print_centered(f"Le lecteur {drive_letter}: n'est pas chiffré ou n'est pas enregistré.", Fore.RED)
            self.get_user_input("Appuyez sur Entrée pour continuer...")
            return

        password = self.get_password("Entrez le mot de passe pour le déchiffrement : ")

        salt = base64.b64decode(self.drives[drive_letter]["salt"])
        key = self.generate_key(password, salt)

        self.print_centered("Déchiffrement en cours...", Fore.YELLOW)

        try:
            for root, dirs, files in os.walk(f"{drive_letter}:\\"):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        self.decrypt_file(file_path, key)
                    except InvalidToken:
                        self.print_centered("Mauvais mot de passe !", Fore.RED)
                        logging.error(f"Incorrect password for drive {drive_letter}")
                        self.get_user_input("Appuyez sur Entrée pour continuer...")
                        return

            self.drives[drive_letter]["is_encrypted"] = False
            self.save_drives()

            self.print_centered("Clé USB déchiffrée avec succès !", Fore.GREEN)
            logging.info(f"Drive {drive_letter}: decrypted successfully")
        except Exception as e:
            self.print_centered("Déchiffrement échoué !", Fore.RED)
            logging.error(f"Error decrypting drive {drive_letter}: {str(e)}")

        self.get_user_input("Appuyez sur Entrée pour continuer...")

    def display_drive_info(self):
        self.clear_screen()
        self.print_banner()
        self.print_centered("Affichage des informations d'une clé USB", Fore.CYAN)
        
        drive_letter = self.get_user_input("Entrez la lettre du lecteur de la clé USB (ex: E): ")
        
        if drive_letter in self.drives:
            self.print_centered(f"Informations pour le lecteur {drive_letter}:", Fore.YELLOW)
            self.print_centered(f"État : {'Chiffré' if self.drives[drive_letter]['is_encrypted'] else 'Non chiffré'}", 
                                Fore.GREEN if self.drives[drive_letter]['is_encrypted'] else Fore.RED)
        else:
            self.print_centered(f"Aucune information sauvegardée pour le lecteur {drive_letter}.", Fore.RED)
        
        self.get_user_input("Appuyez sur Entrée pour continuer...")

    def calculate_additional_space(self):
        self.clear_screen()
        self.print_banner()
        self.print_centered("Calcul de l'espace supplémentaire nécessaire", Fore.CYAN)
        
        drive_letter = self.get_user_input("Entrez la lettre du lecteur de la clé USB (ex: E): ")
        
        if not os.path.exists(f"{drive_letter}:\\"):
            self.print_centered(f"Le lecteur {drive_letter}: n'existe pas.", Fore.RED)
            self.get_user_input("Appuyez sur Entrée pour continuer...")
            return

        self.print_centered("Calcul en cours...", Fore.YELLOW)
        size_difference = self.calculate_size_difference(drive_letter)
        self.print_centered(f"Le chiffrement ajoutera environ {size_difference:.2f} Go.", Fore.GREEN)

        self.get_user_input("Appuyez sur Entrée pour continuer...")

    def main_menu(self):
        options = [
            "Chiffrer une clé USB",
            "Déchiffrer une clé USB",
            "Afficher les informations d'une clé USB",
            "Calculer l'espace supplémentaire nécessaire pour le chiffrement",
            "Quitter"
        ]
        while True:
            self.print_menu("Menu Principal USEBENCY", options)
            choice = self.get_user_choice(len(options))
            if choice == 1:
                self.encrypt_drive()
            elif choice == 2:
                self.decrypt_drive()
            elif choice == 3:
                self.display_drive_info()
            elif choice == 4:
                self.calculate_additional_space()
            elif choice == 5:
                self.print_centered("Au revoir!", Fore.YELLOW)
                break

    def run(self):
        self.show_animation()
        self.main_menu()

if __name__ == "__main__":
    manager = USEBENCYManager()
    manager.run()