import re
import ipaddress
from cryptography.fernet import Fernet

# Fonctions utilitaires
def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def validate_ports(ports_str):
    if re.match(r"^(\d+(-\d+)?)(,\d+(-\d+)?)*$", ports_str):
        return True
    return False

# Chiffrement AES
def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.decrypt(data.encode()).decode()