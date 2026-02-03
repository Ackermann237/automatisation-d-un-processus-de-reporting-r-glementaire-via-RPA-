"""
MOTEUR DE RÈGLES MÉTIER - COMPLIANCE BANCAIRE
BNP Paribas - Projet Automatisation RPA/IA
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

class RulesEngine:
    """Moteur d'application des règles métier de compliance bancaire."""
    
    def __init__(self, config_path=None):
        """Initialise le moteur de règles."""
        if config_path:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = self._get_default_config()
        
        logger.info(f"🔧 Moteur de règles initialisé (seuil: {self.config['seuils']['reglementaire']}€)")
    
    def _get_default_config(self):
        """Retourne la configuration par défaut."""
        return {
            "seuils": {
                "reglementaire": 10000,
                "exceptionnel": 100000,
                "structuring": 9500
            },
            "pays_sanctions": ["RU", "SY", "IR", "KP", "CU", "VE"],
            "coefficients_risque": {
                "PAYS_SANCTIONNE": 100,
                "SEUIL_REGLEMENTAIRE": 30,
                "CLIENT_RISQUE_ELEVE": 25,
                "CLIENT_PEP": 50,
                "MONTANT_EXCEPTIONNEL": 40,
                "SUSPICION_STRUCTURING": 35
            }
        }
    
    def apply_all_rules(self, df_transactions, df_clients=None):
        """Applique l'ensemble des règles métier."""
        logger.info("Application des règles de compliance...")
        
        df = df_transactions.copy()
        df['Alertes'] = ''
        df['Niveau_Alerte'] = 'Faible'
        df['Score_Risque'] = 0
        df['Details_Alertes'] = ''
        
        # Application des règles
        df = self._apply_seuil_reglementaire(df)
        
        if df_clients is not None:
            df = self._apply_risque_client(df, df_clients)
        
        df = self._apply_pays_sanctionnes(df)
        df = self._apply_montant_exceptionnel(df)
        df = self._detect_structuring(df)
        df = self._calculer_niveau_alerte(df)
        
        logger.info("✅ Règles appliquées")
        return df
    
    def _apply_seuil_reglementaire(self, df):
        """Règle 1: Seuil réglementaire."""
        seuil = self.config['seuils']['reglementaire']
        mask = df['Montant'] > seuil
        
        if mask.any():
            df.loc[mask, 'Alertes'] += 'SEUIL_REGLEMENTAIRE;'
            df.loc[mask, 'Score_Risque'] += self.config['coefficients_risque']['SEUIL_REGLEMENTAIRE']
            logger.info(f"   • {mask.sum()} transactions > {seuil}€")
        
        return df
    
    def _apply_risque_client(self, df, df_clients):
        """Règle 2: Risque client."""
        # Fusion temporaire pour les vérifications
        temp_df = pd.merge(
            df[['Transaction_ID', 'Client_ID']],
            df_clients[['Client_ID', 'Niveau_Risque', 'Est_PEP']],
            on='Client_ID',
            how='left'
        )
        
        # Clients à risque élevé
        mask_risque = temp_df['Niveau_Risque'] == 'Élevé'
        if mask_risque.any():
            df.loc[mask_risque, 'Alertes'] += 'CLIENT_RISQUE_ELEVE;'
            df.loc[mask_risque, 'Score_Risque'] += self.config['coefficients_risque']['CLIENT_RISQUE_ELEVE']
            logger.info(f"   • {mask_risque.sum()} clients risque élevé")
        
        # Clients PEP
        mask_pep = temp_df['Est_PEP'] == 'Oui'
        if mask_pep.any():
            df.loc[mask_pep, 'Alertes'] += 'CLIENT_PEP;'
            df.loc[mask_pep, 'Score_Risque'] += self.config['coefficients_risque']['CLIENT_PEP']
            logger.info(f"   • {mask_pep.sum()} clients PEP")
        
        return df
    
    def _apply_pays_sanctionnes(self, df):
        """Règle 3: Pays sous sanctions."""
        mask = df['Pays_Bénéficiaire'].isin(self.config['pays_sanctions'])
        
        if mask.any():
            df.loc[mask, 'Alertes'] += 'PAYS_SANCTIONNE;'
            df.loc[mask, 'Score_Risque'] += self.config['coefficients_risque']['PAYS_SANCTIONNE']
            logger.info(f"   • {mask.sum()} vers pays sanctionnés")
        
        return df
    
    def _apply_montant_exceptionnel(self, df):
        """Règle 4: Montant exceptionnel."""
        seuil = self.config['seuils']['exceptionnel']
        mask = df['Montant'] > seuil
        
        if mask.any():
            df.loc[mask, 'Alertes'] += 'MONTANT_EXCEPTIONNEL;'
            df.loc[mask, 'Score_Risque'] += self.config['coefficients_risque']['MONTANT_EXCEPTIONNEL']
            logger.info(f"   • {mask.sum()} > {seuil}€")
        
        return df
    
    def _detect_structuring(self, df):
        """Règle 5: Détection de structuring."""
        if 'Date' not in df.columns:
            return df
        
        structuring_ids = []
        df['Date_only'] = pd.to_datetime(df['Date']).dt.date
        seuil = self.config['seuils']['structuring']
        
        for (client_id, date), group in df.groupby(['Client_ID', 'Date_only']):
            if len(group) >= 2:
                below = group[group['Montant'] < seuil]
                if len(below) >= 2 and below['Montant'].sum() > 10000:
                    structuring_ids.extend(below.index.tolist())
        
        if structuring_ids:
            df.loc[structuring_ids, 'Alertes'] += 'SUSPICION_STRUCTURING;'
            df.loc[structuring_ids, 'Score_Risque'] += self.config['coefficients_risque']['SUSPICION_STRUCTURING']
            logger.info(f"   • {len(set(structuring_ids))} suspicions structuring")
        
        df = df.drop(columns=['Date_only'], errors='ignore')
        return df
    
    def _calculer_niveau_alerte(self, df):
        """Calcule le niveau d'alerte final."""
        conditions = [
            df['Score_Risque'] >= 100,
            (df['Score_Risque'] >= 70) & (df['Score_Risque'] < 100),
            (df['Score_Risque'] >= 30) & (df['Score_Risque'] < 70),
            df['Score_Risque'] < 30
        ]
        choices = ['Critique', 'Élevé', 'Moyen', 'Faible']
        
        df['Niveau_Alerte'] = np.select(conditions, choices, 'Faible')
        
        # Log distribution
        for niveau in ['Critique', 'Élevé', 'Moyen', 'Faible']:
            count = (df['Niveau_Alerte'] == niveau).sum()
            if count > 0:
                logger.info(f"   • Niveau '{niveau}': {count}")
        
        return df
    
    def generate_summary_report(self, df):
        """Génère un rapport synthétique."""
        summary = {
            "total_transactions": len(df),
            "transactions_alerte": len(df[df['Alertes'] != '']),
            "distribution_niveaux": df['Niveau_Alerte'].value_counts().to_dict(),
            "montant_total_alerte": df.loc[df['Alertes'] != '', 'Montant'].sum() if 'Montant' in df.columns else 0,
            "types_alertes": {}  # ← AJOUTE CETTE LIGNE !
        }
        
        # Calculer les types d'alertes
        if 'Alertes' in df.columns and not df[df['Alertes'] != ''].empty:
            all_alerts = []
            for alerts in df.loc[df['Alertes'] != '', 'Alertes']:
                if isinstance(alerts, str):
                    all_alerts.extend([a.strip() for a in alerts.split(';') if a.strip()])
            
            from collections import Counter
            if all_alerts:
                summary['types_alertes'] = dict(Counter(all_alerts))
        
        return summary
if __name__ == "__main__":
    print("✅ Moteur de règles prêt")