import socket
from utils.logger import Logger
from utils.helpers import validate_ip, validate_ports

class Attack:
    def __init__(self):
        # Initialisation du logger pour ce module
        self.logger = Logger(name="PortScan")

    def setup(self, target_ip, ports="1-1024"):
        # Validation des paramètres d'entrée
        if not validate_ip(target_ip):
            raise ValueError("Adresse IP invalide")
        if not validate_ports(ports):
            raise ValueError("Format de ports invalide")
        
        # Stockage des paramètres pour l'exécution
        self.target_ip = target_ip
        self.ports = self._parse_ports(ports)

    def _parse_ports(self, ports_str):
        """Convertit une chaîne de ports en liste de numéros"""
        ports = []
        # Sépare les différentes parties (ports individuels ou plages)
        for part in ports_str.split(','):
            if '-' in part:
                # Traitement des plages (ex: "80-85")
                start, end = map(int, part.split("-"))
                ports.extend(range(start, end + 1))
            else:
                # Ajout des ports individuels
                ports.append(int(part))
        return ports

    def execute(self):
        """Exécute le scan de ports"""
        open_ports = []
        # Boucle sur chaque port à scanner
        for port in self.ports:
            # Création d'un socket TCP
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # Timeout de 1 seconde
            
            # Tentative de connexion
            result = sock.connect_ex((self.target_ip, port))
            
            if result == 0:  # Code 0 = connexion réussie
                open_ports.append(port)
                self.logger.info(f"Port {port} ouvert")
            
            sock.close()  # Fermeture du socket
        
        return {"open_ports": open_ports}

    def cleanup(self):
        """Nettoyage post-exécution"""
        self.logger.info("Nettoyage des ressources...")