import argparse
import sys
import os
import threading
import base64
import json  # Import manquant ajouté ici
from core.module_loader import load_modules
from core.attack_executor import AttackExecutor
from core.reporting import Reporter
import argcomplete
from api import app as api_app

def main():
    modules = load_modules()
    parser = argparse.ArgumentParser(description="PyRedTeam - Framework d'Attaques Simulées")
    argcomplete.autocomplete(parser)
    
    # Arguments généraux
    parser.add_argument("--list", action="store_true", help="Lister tous les modules")
    parser.add_argument("--run", type=str, help="Nom du module à exécuter")
    parser.add_argument("--target", type=str, help="Cible de l'attaque")
    parser.add_argument("--params", type=str, default="", help="Paramètres supplémentaires au format JSON")
    parser.add_argument("--output", type=str, default="report.json", help="Fichier de sortie")
    parser.add_argument("--encrypt", action="store_true", help="Chiffrer le rapport")
    parser.add_argument("--api", action="store_true", help="Démarrer l'API REST")
    parser.add_argument("--covert", action="store_true", help="Activer le mode discret")
    
    # Arguments spécifiques aux modules
    parser.add_argument("--gateway", type=str, help="Passerelle pour ARP Spoof")
    parser.add_argument("--interface", type=str, default="eth0", help="Interface réseau")
    parser.add_argument("--ports", type=str, help="Ports à scanner")
    parser.add_argument("--url", type=str, help="URL pour les attaques web")
    parser.add_argument("--command", type=str, help="Commande à exécuter")

    args = parser.parse_args()

    if args.api:
        api_thread = threading.Thread(
            target=api_app.run, 
            kwargs={'host': '0.0.0.0', 'port': 5000, 'ssl_context': 'adhoc'}
        )
        api_thread.daemon = True
        api_thread.start()
        print("API REST démarrée sur https://0.0.0.0:5000")
        api_thread.join()

    if args.list:
        print("Modules disponibles:")
        for name in modules.keys():
            print(f"- {name}")
        return

    if args.run and args.target:
        # Paramètres communs à tous les modules
        base_params = {
            'target_ip': args.target,
            'covert': args.covert
        }
        
        # Paramètres spécifiques aux modules
        module_params = {}
        
        if args.run == "arp_spoof":
            if not args.gateway:
                print("Erreur: --gateway requis pour ARP Spoof")
                sys.exit(1)
            module_params = {
                'gateway_ip': args.gateway,
                'interface': args.interface
            }
        
        elif args.run == "port_scan":
            module_params = {
                'ports': args.ports or "1-1024"
            }
        
        elif args.run == "password_spray":
            if not args.url:
                print("Erreur: --url requis pour Password Spray")
                sys.exit(1)
            module_params = {
                'target_url': args.url
            }
        
        # Fusion des paramètres
        params = {**base_params, **module_params}
        
        # Ajout des paramètres supplémentaires au format JSON
        if args.params:
            try:
                extra_params = json.loads(args.params)
                params.update(extra_params)
            except json.JSONDecodeError as e:
                print(f"ERREUR: Format JSON invalide pour --params: {args.params}")
                print(f"Détails: {str(e)}")
                sys.exit(1)
        
        executor = AttackExecutor(modules)
        try:
            result = executor.run(args.run, **params)
            
            encrypt_key = None
            if args.encrypt:
                encrypt_key = base64.urlsafe_b64encode(os.urandom(32)).decode()
            
            report = Reporter.generate_report(args.run, result, encrypt_key=encrypt_key)
            Reporter.save_report(report, args.output, encrypt_key=encrypt_key)
            
            if args.encrypt:
                print(f"Rapport chiffré sauvegardé. Clé de déchiffrement: {encrypt_key}")
            else:
                print(f"Rapport généré: {args.output}")
                
        except Exception as e:
            print(f"Erreur: {str(e)}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()