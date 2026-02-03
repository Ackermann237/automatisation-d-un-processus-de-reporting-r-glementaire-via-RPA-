"""
DATA PROCESSOR - Traitement des données bancaires
BNP Paribas - Projet Automatisation RPA/IA
Auteur : [Ton Nom]
Description : Module de chargement, nettoyage et enrichissement des données.
"""

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    """
    Processeur de données pour le pipeline de compliance.
    Gère le chargement, validation, nettoyage et enrichissement.
    """
    
    def __init__(self):
        """Initialise le processeur de données."""
        self.transactions_df = None
        self.clients_df = None
        self.enriched_df = None
        
    def load_transactions(self, filepath, sep=';'):
        """
        Charge le fichier de transactions.
        
        Args:
            filepath (str): Chemin vers le fichier CSV
            sep (str): Séparateur (par défaut ';')
            
        Returns:
            DataFrame: Transactions chargées
        """
        try:
            self.transactions_df = pd.read_csv(filepath, sep=sep)
            logger.info(f"✅ Transactions chargées : {len(self.transactions_df)} lignes")
            return self.transactions_df
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement des transactions : {str(e)}")
            raise
    
    def load_clients(self, filepath, sep=';'):
        """
        Charge le fichier des clients.
        
        Args:
            filepath (str): Chemin vers le fichier CSV
            sep (str): Séparateur (par défaut ';')
            
        Returns:
            DataFrame: Clients chargés
        """
        try:
            self.clients_df = pd.read_csv(filepath, sep=sep)
            logger.info(f"✅ Clients chargés : {len(self.clients_df)} lignes")
            return self.clients_df
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement des clients : {str(e)}")
            raise
    
    def validate_data(self):
        """
        Valide l'intégrité des données chargées.
        
        Returns:
            dict: Résultats de la validation
        """
        validation_results = {
            'transactions_valid': False,
            'clients_valid': False,
            'errors': [],
            'warnings': []
        }
        
        # Validation des transactions
        if self.transactions_df is not None:
            required_transaction_cols = ['Transaction_ID', 'Client_ID', 'Montant', 'Pays_Bénéficiaire']
            missing_cols = [col for col in required_transaction_cols 
                          if col not in self.transactions_df.columns]
            
            if missing_cols:
                error_msg = f"Colonnes manquantes dans transactions : {missing_cols}"
                validation_results['errors'].append(error_msg)
            else:
                validation_results['transactions_valid'] = True
            
            # Vérification des valeurs manquantes
            missing_ids = self.transactions_df['Transaction_ID'].isnull().sum()
            if missing_ids > 0:
                warning_msg = f"⚠️  {missing_ids} Transaction_ID manquants"
                validation_results['warnings'].append(warning_msg)
        
        # Validation des clients
        if self.clients_df is not None:
            required_client_cols = ['Client_ID', 'Niveau_Risque', 'Est_PEP']
            missing_cols = [col for col in required_client_cols 
                          if col not in self.clients_df.columns]
            
            if missing_cols:
                error_msg = f"Colonnes manquantes dans clients : {missing_cols}"
                validation_results['errors'].append(error_msg)
            else:
                validation_results['clients_valid'] = True
            
            # Vérification des valeurs manquantes
            missing_ids = self.clients_df['Client_ID'].isnull().sum()
            if missing_ids > 0:
                warning_msg = f"⚠️  {missing_ids} Client_ID manquants"
                validation_results['warnings'].append(warning_msg)
        
        # Log des résultats
        if validation_results['errors']:
            for error in validation_results['errors']:
                logger.error(error)
        
        if validation_results['warnings']:
            for warning in validation_results['warnings']:
                logger.warning(warning)
        
        if validation_results['transactions_valid'] and validation_results['clients_valid']:
            logger.info("✅ Validation des données terminée avec succès")
        
        return validation_results
    
    def clean_transactions(self):
        """
        Nettoie les données de transactions.
        
        Returns:
            DataFrame: Transactions nettoyées
        """
        if self.transactions_df is None:
            raise ValueError("Les transactions doivent être chargées avant le nettoyage")
        
        logger.info("Nettoyage des transactions...")
        
        # Sauvegarde du nombre initial
        initial_count = len(self.transactions_df)
        
        # 1. Conversion des types de données
        self.transactions_df['Montant'] = pd.to_numeric(
            self.transactions_df['Montant'], errors='coerce'
        )
        
        if 'Date' in self.transactions_df.columns:
            self.transactions_df['Date'] = pd.to_datetime(
                self.transactions_df['Date'], errors='coerce'
            )
        
        # 2. Suppression des doublons
        self.transactions_df = self.transactions_df.drop_duplicates(
            subset=['Transaction_ID']
        )
        duplicates_removed = initial_count - len(self.transactions_df)
        
        if duplicates_removed > 0:
            logger.info(f"   • {duplicates_removed} doublons supprimés")
        
        # 3. Gestion des valeurs manquantes
        numeric_cols = self.transactions_df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            missing = self.transactions_df[col].isnull().sum()
            if missing > 0:
                # Pour les montants, on ne remplit pas, on garde NaN
                logger.debug(f"   • {missing} valeurs manquantes dans {col}")
        
        # 4. Filtrage des données aberrantes (montants négatifs)
        negative_mask = self.transactions_df['Montant'] < 0
        if negative_mask.any():
            logger.warning(f"   • {negative_mask.sum()} transactions avec montant négatif")
            # Optionnel : les supprimer ou les marquer
            # self.transactions_df = self.transactions_df[~negative_mask]
        
        logger.info(f"✅ Nettoyage terminé : {len(self.transactions_df)} transactions valides")
        
        return self.transactions_df
    
    def enrich_data(self):
        """
        Enrichit les transactions avec les informations clients.
        
        Returns:
            DataFrame: Données enrichies
        """
        if self.transactions_df is None or self.clients_df is None:
            raise ValueError("Les transactions et clients doivent être chargés")
        
        logger.info("Enrichissement des données...")
        
        # Sélection des colonnes clients nécessaires
        client_cols = ['Client_ID', 'Niveau_Risque', 'Est_PEP', 'Pays', 'Segment']
        available_cols = [col for col in client_cols if col in self.clients_df.columns]
        
        # Jointure
        self.enriched_df = pd.merge(
            self.transactions_df,
            self.clients_df[available_cols],
            on='Client_ID',
            how='left',
            suffixes=('', '_client')
        )
        
        # Statistiques sur l'enrichissement
        missing_clients = self.enriched_df['Client_ID'].isin(self.clients_df['Client_ID']).sum()
        matched_percentage = (missing_clients / len(self.enriched_df)) * 100
        
        logger.info(f"   • {missing_clients}/{len(self.enriched_df)} transactions liées à un client ({matched_percentage:.1f}%)")
        
        # Valeurs par défaut pour les clients non trouvés
        if 'Niveau_Risque' in self.enriched_df.columns:
            missing_risk = self.enriched_df['Niveau_Risque'].isnull().sum()
            if missing_risk > 0:
                self.enriched_df['Niveau_Risque'].fillna('Inconnu', inplace=True)
                logger.info(f"   • {missing_risk} transactions avec risque client inconnu")
        
        if 'Est_PEP' in self.enriched_df.columns:
            missing_pep = self.enriched_df['Est_PEP'].isnull().sum()
            if missing_pep > 0:
                self.enriched_df['Est_PEP'].fillna('Non', inplace=True)
        
        logger.info(f"✅ Données enrichies : {len(self.enriched_df)} transactions")
        
        return self.enriched_df
    
    def get_summary_stats(self):
        """
        Génère des statistiques descriptives sur les données.
        
        Returns:
            dict: Statistiques
        """
        stats = {}
        
        if self.transactions_df is not None:
            stats['transactions'] = {
                'count': len(self.transactions_df),
                'montant_total': self.transactions_df['Montant'].sum(),
                'montant_moyen': self.transactions_df['Montant'].mean(),
                'montant_max': self.transactions_df['Montant'].max(),
                'montant_min': self.transactions_df['Montant'].min(),
                'period_min': self.transactions_df['Date'].min() if 'Date' in self.transactions_df.columns else None,
                'period_max': self.transactions_df['Date'].max() if 'Date' in self.transactions_df.columns else None
            }
        
        if self.clients_df is not None:
            stats['clients'] = {
                'count': len(self.clients_df),
                'par_risque': self.clients_df['Niveau_Risque'].value_counts().to_dict() if 'Niveau_Risque' in self.clients_df.columns else {},
                'pep_count': (self.clients_df['Est_PEP'] == 'Oui').sum() if 'Est_PEP' in self.clients_df.columns else 0
            }
        
        if self.enriched_df is not None:
            stats['enriched'] = {
                'count': len(self.enriched_df),
                'transactions_avec_client': self.enriched_df['Client_ID'].isin(self.clients_df['Client_ID']).sum()
            }
        
        return stats