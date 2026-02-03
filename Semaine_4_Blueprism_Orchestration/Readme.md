# SEMAIRE 4 - ORCHESTRATION RPA POUR BNP

## RÉSUMEX DU PROJET
Intégration Blue Prism + Python pour l'automatisation de la surveillance réglementaire.

## ARCHITECTURE


## RÉSULTATS CONCRETS
### Métriques de performance :
- **Temps d'exécution** : 0.105 seconde (vs. 2-3 heures manuellement)
- **Transactions analysées** : 60
- **Alertes détectées** : 53 (88.3% de taux)
- **Alertes critiques** : 4 transactions
- **Montant à risque identifié** : 1 889 325,43 €

### Règles de compliance appliquées :
1. Seuil réglementaire (>10 000€) : 48 transactions
2. Clients à risque élevé : 23 transactions
3. Clients PEP : 2 transactions
4. Pays sous sanctions : 2 transactions
5. Montant exceptionnel (>100 000€) : 3 transactions

## FICHIERS GÉNÉRÉS
- `alertes_compliance.csv` : 53 transactions suspectes triées par risque
- `rapport_detaille.csv` : Statistiques complètes du traitement
- `transactions_enrichies.csv` : Base enrichie pour analyse future
- `statistiques_pipeline.json` : Données structurées pour intégration

## ORCHESTRATION AVEC BLUE PRISM
### Processus conçu :
1. Déclenchement automatique à 8h00
2. Exécution du pipeline Python
3. Vérification des résultats
4. Notification des alertes critiques
5. Reporting d'exécution

### Interface technique :

Commande : python pipeline.py
Entrée : transactions.csv, clients.csv
Sortie : alertes_compliance.csv
Codes retour : 0=Succès, 1=Erreur données, 2=Erreur traitement