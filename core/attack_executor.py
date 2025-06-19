# Orchestrateur d'exécution des modules
class AttackExecutor:
    def __init__(self, modules):
        self.modules = modules  # Modules chargés
       
    def run(self, module_name, **kwargs):
        if module_name not in self.modules:
            raise ValueError(f"Module inconnu: {module_name}")
       
        attack = self.modules[module_name]()  # Instanciation
        attack.setup(**kwargs)   # Initialisation
        result = attack.execute()  # Exécution
        attack.cleanup()  # Nettoyage
        return result