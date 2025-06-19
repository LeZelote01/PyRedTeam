import logging
from logging.handlers import RotatingFileHandler
import os
import json
from elasticsearch import Elasticsearch
import warnings

class Logger:
    def __init__(self, name, log_level="INFO", elastic_config=None):
        # Création directe du logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        # Configuration commune
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Handler console
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        
        # Handler fichier
        os.makedirs("logs", exist_ok=True)
        fh = RotatingFileHandler(
            f"logs/{name}.log",
            maxBytes=10*1024*1024,
            backupCount=5
        )
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        
        # Handler ElasticSearch (optionnel)
        if elastic_config:
            try:
                from elasticsearch_logging import ElasticsearchHandler
                
                # Configuration ES
                es = Elasticsearch(
                    [elastic_config['host']],
                    verify_certs=False,
                    ssl_show_warn=False
                )
                es_handler = ElasticsearchHandler(
                    es,
                    index_name=elastic_config['index'],
                    index_rotate="daily"
                )
                es_handler.setFormatter(formatter)
                self.logger.addHandler(es_handler)
            except ImportError:
                self.logger.error("Module elasticsearch-logging-handler non installé")
            except Exception as e:
                self.logger.error(f"Erreur ElasticSearch: {str(e)}")
    
    # Méthodes proxy pour une utilisation plus naturelle
    def info(self, message, extra=None):
        if extra:
            self.logger.info(f"{message} | {json.dumps(extra)}")
        else:
            self.logger.info(message)
    
    def error(self, message, extra=None):
        if extra:
            self.logger.error(f"{message} | {json.dumps(extra)}")
        else:
            self.logger.error(message)
    
    def warning(self, message, extra=None):
        if extra:
            self.logger.warning(f"{message} | {json.dumps(extra)}")
        else:
            self.logger.warning(message)