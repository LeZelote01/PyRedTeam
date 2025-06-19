import importlib.util
import os

# Charge dynamiquement les modules
def load_modules(module_dir="modules"):
    modules = {}
    for root, _, files in os.walk(module_dir):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                module_path = os.path.join(root, file)
                module_name = os.path.splitext(file)[0]
               
                # Chargement dynamique
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
               
                # Vérifie la présence de la classe Attack
                if hasattr(module, "Attack"):
                    modules[module_name] = module.Attack
    return modules