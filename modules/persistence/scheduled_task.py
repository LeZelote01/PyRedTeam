import subprocess
from utils.logger import Logger

class Attack:
    def __init__(self):
        # Initialisation du logger
        self.logger = Logger("ScheduledTask")

    def setup(self, task_name, command, trigger="hourly", **kwargs):
        """Configuration de la tâche"""
        # Stockage des paramètres
        self.task_name = task_name
        self.command = command    # Commande à exécuter
        self.trigger = trigger    # Fréquence d'exécution

    def execute(self):
        """Création de la tâche planifiée"""
        try:
            # Commande schtasks pour créer la tâche
            subprocess.run(
                f'schtasks /create /tn "{self.task_name}" /tr "{self.command}" /sc {self.trigger}',
                shell=True,
                check=True  # Lève une exception en cas d'erreur
            )
            self.logger.info(f"Tâche planifiée créée: {self.task_name}")
            return {"status": "success"}
        
        except subprocess.CalledProcessError as e:
            # Gestion des erreurs
            self.logger.error(f"Erreur: {str(e)}")
            return {"status": "failed", "error": str(e)}

    def cleanup(self):
        """Suppression de la tâche planifiée"""
        try:
            # Commande schtasks pour supprimer la tâche
            subprocess.run(
                f'schtasks /delete /tn "{self.task_name}" /f',
                shell=True,
                check=True
            )
            self.logger.info(f"Tâche planifiée supprimée: {self.task_name}")
        
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Erreur lors du nettoyage: {str(e)}")