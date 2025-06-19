from flask import Flask, request, jsonify
from core.module_loader import load_modules
from core.attack_executor import AttackExecutor
import threading
import time

app = Flask(__name__)
executor = AttackExecutor(load_modules())
active_attacks = {}  # Suivi des attaques en cours

# Liste des modules disponibles
@app.route('/attacks', methods=['GET'])
def list_attacks():
    return jsonify({"modules": list(executor.modules.keys())})

# Exécution d'une attaque
@app.route('/attack/<module_name>', methods=['POST'])
def run_attack(module_name):
    params = request.json
    thread = threading.Thread(target=_execute_attack, args=(module_name, params))
    thread.start()
    active_attacks[thread.ident] = thread
    return jsonify({"status": "started", "attack_id": thread.ident})

# Fonction interne d'exécution
def _execute_attack(module_name, params):
    try:
        result = executor.run(module_name, **params)
        app.logger.info(f"Attaque {module_name} terminée")
    except Exception as e:
        app.logger.error(f"Échec: {str(e)}")

# Arrêt d'une attaque
@app.route('/attack/<int:attack_id>', methods=['DELETE'])
def stop_attack(attack_id):
    if attack_id in active_attacks:
        active_attacks[attack_id].join(timeout=10)
        if active_attacks[attack_id].is_alive():
            return jsonify({"error": "Échec de l'arrêt"}), 500
        del active_attacks[attack_id]
        return jsonify({"status": "stopped"})
    return jsonify({"error": "Attaque non trouvée"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')  # HTTPS auto-signé