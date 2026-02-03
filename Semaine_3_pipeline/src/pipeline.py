"""
PIPELINE DE TRAITEMENT POUR LA SURVEILLANCE RÉGLEMENTAIRE
BNP Paribas - Projet Automatisation RPA/IA
Version finale corrigée pour Windows
"""

import pandas as pd
import numpy as np
from datetime import datetime
import logging
import sys
import os
import json

# Import des modules personnalisés
from data_processor import DataProcessor
from rules_engine import RulesEngine

# Configuration du logging SANS ÉMOJIS pour Windows
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline_execution.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class CompliancePipeline:
    """Pipeline principal de traitement des données de compliance."""
    
    def __init__(self, transactions_path, clients_path, output_dir='../output'):
        """
        Initialise le pipeline avec les chemins des fichiers.
        
        Args:
            transactions_path (str): Chemin vers le fichier transactions
            clients_path (str): Chemin vers le fichier clients
            output_dir (str): Répertoire de sortie
        """
        self.transactions_path = transactions_path
        self.clients_path = clients_path
        self.output_dir = output_dir
        
        # Initialisation des modules
        self.data_processor = DataProcessor()
        self.rules_engine = None
        self.enriched_df = None
        self.alerts_df = None
        self.summary_stats = {}
        
        # Création du répertoire de sortie si inexistant
        os.makedirs(output_dir, exist_ok=True)
        
    def load_config(self):
        """Charge la configuration des règles métier."""
        config_path = "./config/rules_config.json"
        try:
            if os.path.exists(config_path):
                self.rules_engine = RulesEngine(config_path)
                logger.info("Configuration des règles chargée")
            else:
                self.rules_engine = RulesEngine()  # Configuration par défaut
                logger.warning("Configuration par défaut utilisée")
        except Exception as e:
            logger.error(f"Erreur lors du chargement de la configuration : {str(e)}")
            self.rules_engine = RulesEngine()
    
    def load_and_validate_data(self):
        """Charge et valide les données sources."""
        logger.info("=" * 40)
        logger.info("CHARGEMENT ET VALIDATION DES DONNEES")
        logger.info("=" * 40)
        
        try:
            # 1. Chargement des données
            self.data_processor.load_transactions(self.transactions_path)
            self.data_processor.load_clients(self.clients_path)
            
            # 2. Validation
            validation_results = self.data_processor.validate_data()
            
            if validation_results['errors']:
                logger.error("Echec de la validation des données")
                return False
            
            # 3. Statistiques initiales
            self.summary_stats['initial'] = self.data_processor.get_summary_stats()
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement : {str(e)}")
            return False
    
    def clean_and_enrich_data(self):
        """Nettoie et enrichit les données."""
        logger.info("=" * 40)
        logger.info("NETTOYAGE ET ENRICHISSEMENT")
        logger.info("=" * 40)
        
        try:
            # 1. Nettoyage des transactions
            self.data_processor.clean_transactions()
            
            # 2. Enrichissement avec les données clients
            self.enriched_df = self.data_processor.enrich_data()
            
            # 3. Statistiques après enrichissement
            self.summary_stats['enriched'] = self.data_processor.get_summary_stats()
            
            logger.info("Donnees nettoyees et enrichies avec succes")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement des données : {str(e)}")
            return False
    
    def apply_compliance_rules(self):
        """Applique les règles métier de compliance."""
        logger.info("=" * 40)
        logger.info("APPLICATION DES REGLES DE COMPLIANCE")
        logger.info("=" * 40)
        
        try:
            # Chargement de la configuration si pas déjà fait
            if self.rules_engine is None:
                self.load_config()
            
            # Application des règles
            self.enriched_df = self.rules_engine.apply_all_rules(
                self.enriched_df, 
                self.data_processor.clients_df
            )
            
            # Génération du rapport synthétique
            rules_summary = self.rules_engine.generate_summary_report(self.enriched_df)
            self.summary_stats['rules'] = rules_summary
            
            # Création du DataFrame d'alertes
            self.alerts_df = self.enriched_df[
                self.enriched_df['Alertes'] != ''
            ].copy()
            
            # Tri par priorité
            if len(self.alerts_df) > 0:
                priority_order = {'Critique': 3, 'Eleve': 2, 'Moyen': 1, 'Faible': 0}
                self.alerts_df['Priority_Score'] = self.alerts_df['Niveau_Alerte'].map(priority_order)
                self.alerts_df = self.alerts_df.sort_values(
                    ['Priority_Score', 'Score_Risque'], 
                    ascending=[False, False]
                ).drop(columns=['Priority_Score'])
            
            # Log des résultats
            logger.info("RESUME DES ALERTES DETECTEES :")
            logger.info(f"   - Transactions totales : {rules_summary['total_transactions']}")
            logger.info(f"   - Transactions avec alerte : {rules_summary['transactions_alerte']}")
            logger.info(f"   - Pourcentage d'alertes : {(rules_summary['transactions_alerte']/rules_summary['total_transactions']*100):.1f}%")
            logger.info(f"   - Montant total a risque : {rules_summary['montant_total_alerte']:,.2f} EUR")
            
            for niveau, count in rules_summary['distribution_niveaux'].items():
                logger.info(f"   - Niveau '{niveau}' : {count}")
            
            logger.info("Regles de compliance appliquees avec succes")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'application des regles : {str(e)}")
            return False
    
    def generate_reports(self):
        """Génère les rapports et fichiers de sortie."""
        logger.info("=" * 40)
        logger.info("GENERATION DES RAPPORTS")
        logger.info("=" * 40)
        
        try:
            # 1. Fichier complet avec toutes les transactions enrichies
            output_path_all = os.path.join(self.output_dir, 'transactions_enrichies.csv')
            self.enriched_df.to_csv(output_path_all, sep=';', index=False, encoding='utf-8')
            logger.info(f"Fichier complet genere : {output_path_all}")
            
            # 2. Fichier d'alertes seulement (pour les analystes compliance)
            if self.alerts_df is not None and len(self.alerts_df) > 0:
                output_path_alerts = os.path.join(self.output_dir, 'alertes_compliance.csv')
                
                # Sélection des colonnes importantes
                alertes_cols = [
                    'Transaction_ID', 'Date', 'Client_ID', 'Montant', 'Devise',
                    'Beneficiaire', 'Pays_Beneficiaire', 'Niveau_Risque', 'Est_PEP',
                    'Alertes', 'Niveau_Alerte', 'Score_Risque', 'Details_Alertes'
                ]
                
                # S'assurer que toutes les colonnes existent
                available_cols = [col for col in alertes_cols if col in self.alerts_df.columns]
                self.alerts_df[available_cols].to_csv(
                    output_path_alerts, sep=';', index=False, encoding='utf-8'
                )
                
                logger.info(f"Fichier d'alertes genere : {output_path_alerts}")
                logger.info(f"   - {len(self.alerts_df)} alertes exportees")
            
            # 3. Rapport synthétique détaillé
            self._generate_detailed_report()
            
            # 4. Fichier JSON avec toutes les statistiques (pour dashboard) - CORRIGÉ
            self._generate_stats_json()
            
            logger.info("Generation des rapports terminee")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la generation des rapports : {str(e)}")
            return False
    
    def _generate_detailed_report(self):
        """Génère un rapport synthétique détaillé."""
        report_data = []
        
        # 1. Statistiques générales
        if 'initial' in self.summary_stats:
            stats = self.summary_stats['initial']
            report_data.append(['GENERAL', 'Transactions totales', stats['transactions']['count']])
            report_data.append(['GENERAL', 'Clients total', stats['clients']['count']])
            report_data.append(['GENERAL', 'Montant total', f"{stats['transactions']['montant_total']:,.2f} EUR"])
            report_data.append(['GENERAL', 'Montant moyen', f"{stats['transactions']['montant_moyen']:,.2f} EUR"])
        
        # 2. Statistiques des règles
        if 'rules' in self.summary_stats:
            rules = self.summary_stats['rules']
            report_data.append(['REGLES', 'Transactions avec alerte', rules['transactions_alerte']])
            report_data.append(['REGLES', 'Montant a risque', f"{rules['montant_total_alerte']:,.2f} EUR"])
            
            for niveau, count in rules['distribution_niveaux'].items():
                report_data.append(['NIVEAUX ALERTE', f"Niveau {niveau}", count])
            
            # Vérification que 'types_alertes' existe
            if 'types_alertes' in rules and rules['types_alertes']:
                for alerte_type, count in rules['types_alertes'].items():
                    report_data.append(['TYPES ALERTE', alerte_type, count])
        
        # 3. Export en CSV
        if report_data:
            report_df = pd.DataFrame(report_data, columns=['Categorie', 'Metrique', 'Valeur'])
            report_path = os.path.join(self.output_dir, 'rapport_detaille.csv')
            report_df.to_csv(report_path, sep=';', index=False, encoding='utf-8')
            logger.info(f"Rapport detaille genere : {report_path}")
    
    def _generate_stats_json(self):
        """Génère un fichier JSON avec toutes les statistiques (pour intégration dashboard)."""
        json_path = os.path.join(self.output_dir, 'statistiques_pipeline.json')
        
        # Conversion des types NumPy en types Python natifs pour JSON
        def convert_to_serializable(obj):
            if isinstance(obj, (np.integer, np.int64, np.int32)):
                return int(obj)
            elif isinstance(obj, (np.floating, np.float64, np.float32)):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, pd.Timestamp):
                return obj.isoformat()
            elif isinstance(obj, dict):
                return {key: convert_to_serializable(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_serializable(item) for item in obj]
            else:
                return obj
        
        # Préparation des données pour JSON
        json_data = {
            'timestamp': datetime.now().isoformat(),
            'pipeline_version': '1.0',
            'statistiques': convert_to_serializable(self.summary_stats),
            'fichiers_generes': [
                'transactions_enrichies.csv',
                'alertes_compliance.csv',
                'rapport_detaille.csv'
            ]
        }
        
        # Ajout des métadonnées de traitement
        if self.alerts_df is not None and not self.alerts_df.empty:
            json_data['alertes'] = {
                'total': int(len(self.alerts_df)),
                'par_niveau': convert_to_serializable(self.alerts_df['Niveau_Alerte'].value_counts().to_dict()),
            }
        
        # Export JSON
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2, default=str)
            logger.info(f"Statistiques JSON generees : {json_path}")
        except Exception as e:
            logger.error(f"Erreur lors de la generation du JSON : {str(e)}")
            # On ne bloque pas le pipeline pour cette erreur
    
    def run_pipeline(self):
        """Exécute l'ensemble du pipeline de traitement."""
        logger.info("=" * 60)
        logger.info("DEMARRAGE DU PIPELINE DE COMPLIANCE BNP")
        logger.info("=" * 60)
        
        start_time = datetime.now()
        execution_steps = {}
        
        try:
            # Étape 1: Chargement configuration
            step_start = datetime.now()
            self.load_config()
            execution_steps['config'] = (datetime.now() - step_start).total_seconds()
            
            # Étape 2: Chargement et validation
            step_start = datetime.now()
            if not self.load_and_validate_data():
                return False
            execution_steps['load'] = (datetime.now() - step_start).total_seconds()
            
            # Étape 3: Nettoyage et enrichissement
            step_start = datetime.now()
            if not self.clean_and_enrich_data():
                return False
            execution_steps['clean'] = (datetime.now() - step_start).total_seconds()
            
            # Étape 4: Application des règles
            step_start = datetime.now()
            if not self.apply_compliance_rules():
                return False
            execution_steps['rules'] = (datetime.now() - step_start).total_seconds()
            
            # Étape 5: Génération des rapports
            step_start = datetime.now()
            if not self.generate_reports():
                # On continue même si les rapports ont des problèmes mineurs
                logger.warning("Problemes mineurs dans la generation des rapports, mais traitement principal reussi")
            execution_steps['reports'] = (datetime.now() - step_start).total_seconds()
            
            # Calcul du temps total
            total_time = (datetime.now() - start_time).total_seconds()
            
            # Rapport d'exécution final
            logger.info("=" * 60)
            logger.info("PIPELINE TERMINE AVEC SUCCES")
            logger.info("=" * 60)
            logger.info(f"TEMPS D'EXECUTION DETAILLE :")
            logger.info(f"   - Configuration : {execution_steps['config']:.3f}s")
            logger.info(f"   - Chargement : {execution_steps['load']:.3f}s")
            logger.info(f"   - Nettoyage : {execution_steps['clean']:.3f}s")
            logger.info(f"   - Regles : {execution_steps['rules']:.3f}s")
            logger.info(f"   - Rapports : {execution_steps['reports']:.3f}s")
            logger.info(f"   - TOTAL : {total_time:.3f}s")
            logger.info("")
            logger.info(f"RESULTATS FINAUX :")
            logger.info(f"   - Transactions traitees : {len(self.enriched_df)}")
            logger.info(f"   - Alertes generees : {len(self.alerts_df) if self.alerts_df is not None else 0}")
            
            if 'rules' in self.summary_stats:
                rules_stats = self.summary_stats['rules']
                if 'transactions_alerte' in rules_stats:
                    percentage = (rules_stats['transactions_alerte'] / len(self.enriched_df)) * 100
                    logger.info(f"   - Taux d'alerte : {percentage:.1f}%")
            
            logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            logger.error(f"Echec critique du pipeline : {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return False

# Point d'entrée principal
if __name__ == "__main__":
    # Chemins vers les fichiers de données
    # MODIFIE CES CHEMINS SELON TON ENVIRONNEMENT
    transactions_path = "../src/data/transactions.csv"
    clients_path = "../src/data/clients.csv"
    
 
    
    # Création et exécution du pipeline
    pipeline = CompliancePipeline(transactions_path, clients_path)
    success = pipeline.run_pipeline()
    
    # Code de sortie
    sys.exit(0 if success else 1)