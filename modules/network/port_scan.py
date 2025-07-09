import socket
import time
from utils.logger import Logger
from utils.helpers import validate_ip, validate_ports

class Attack:
    def __init__(self):
        # Initialisation correcte du logger
        self.logger = Logger(name="PortScan").logger  # Accès à l'objet logger interne
        self.target_ip = None
        self.ports = []
        self.start_time = None
        self.logger.info("Module PortScan initialisé")  # Test de journalisation

    def setup(self, target_ip, ports="1-1024", **kwargs):
        """Configure le scan de ports avec validation des paramètres"""
        self.logger.info(f"Configuration du scan: target={target_ip}, ports={ports}")
        
        # Validation des paramètres essentiels
        if not validate_ip(target_ip):
            raise ValueError("Adresse IP invalide")
        if not validate_ports(ports):
            raise ValueError("Format de ports invalide")
        
        # Stockage des paramètres
        self.target_ip = target_ip
        self.ports = self._parse_ports(ports)
        
        # Avertissement pour les paramètres supplémentaires
        if kwargs:
            self.logger.warning(f"Paramètres supplémentaires ignorés: {', '.join(kwargs.keys())}")

    def _parse_ports(self, ports_str):
        """Convertit une chaîne de ports en liste de numéros avec validation"""
        ports = []
        
        for part in ports_str.split(','):
            if '-' in part:
                # Traitement des plages (ex: "80-85")
                start, end = map(int, part.split("-"))
                if not (1 <= start <= 65535) or not (1 <= end <= 65535):
                    raise ValueError("Ports doivent être entre 1 et 65535")
                ports.extend(range(start, end + 1))
            else:
                # Ajout des ports individuels
                port = int(part)
                if not (1 <= port <= 65535):
                    raise ValueError(f"Port invalide: {port}")
                ports.append(port)
        return sorted(set(ports))  # Élimine les doublons et trie

    def execute(self):
        """Exécute le scan de ports avec gestion du temps et des erreurs"""
        if not self.target_ip or not self.ports:
            raise RuntimeError("Module non configuré correctement")
        
        self.start_time = time.time()
        open_ports = []
        total_ports = len(self.ports)
        
        self.logger.info(f"Début du scan sur {self.target_ip} ({total_ports} ports)")
        
        for i, port in enumerate(self.ports):
            try:
                # Création d'un socket TCP
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(1.0)  # Timeout de 1 seconde
                    
                    # Tentative de connexion
                    result = sock.connect_ex((self.target_ip, port))
                    
                    if result == 0:  # Code 0 = connexion réussie
                        open_ports.append(port)
                        self.logger.info(f"Port {port}/TCP ouvert")
                    
                    # Journalisation périodique
                    if (i + 1) % 50 == 0 or (i + 1) == total_ports:
                        elapsed = time.time() - self.start_time
                        self.logger.info(
                            f"Progression: {i+1}/{total_ports} ports "
                            f"({(i+1)/total_ports:.0%}) - "
                            f"{elapsed:.1f}s écoulées"
                        )
            
            except Exception as e:
                self.logger.error(f"Erreur sur le port {port}: {str(e)}")
        
        # Résumé final
        scan_duration = time.time() - self.start_time
        self.logger.info(
            f"Scan terminé: {len(open_ports)} ports ouverts sur {total_ports} "
            f"scannés en {scan_duration:.2f} secondes"
        )
        
        return {
            "target": self.target_ip,
            "open_ports": sorted(open_ports),
            "total_ports_scanned": total_ports,
            "scan_duration": round(scan_duration, 2)
        }

    def cleanup(self):
        """Nettoyage post-exécution"""
        self.logger.info("Nettoyage des ressources du scan...")
        # Réinitialisation pour une éventuelle réutilisation
        self.target_ip = None
        self.ports = []
        self.start_time = None