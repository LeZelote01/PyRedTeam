import json
import yaml
import datetime
from utils import helpers

# Gestion des rapports
class Reporter:
    @staticmethod
    def generate_report(attack_name, results, output_format="json", encrypt_key=None):
        report = {
            "timestamp": str(datetime.datetime.utcnow()),
            "attack": attack_name,
            "results": results
        }
       
        # Formats de sortie
        if output_format == "json":
            output = json.dumps(report, indent=4)
        elif output_format == "yaml":
            output = yaml.dump(report, sort_keys=False)
        elif output_format == "html":
            output = f"<html><body><h1>Rapport: {attack_name}</h1><pre>{json.dumps(results, indent=4)}</pre></body></html>"
        
        # Chiffrement
        if encrypt_key:
            output = helpers.encrypt_data(output, encrypt_key)
        return output

    @staticmethod
    def save_report(report, filename, encrypt_key=None):
        mode = "wb" if encrypt_key else "w"
        with open(filename, mode) as f:
            if encrypt_key:
                f.write(report.encode())
            else:
                f.write(report)