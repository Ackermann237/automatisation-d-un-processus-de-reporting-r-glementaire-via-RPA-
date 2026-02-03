# INTERFACE POUR ÉQUIPE RPA BNP

## CONTRAT TECHNIQUE : PIPELINE PYTHON

**Script à appeler** : `pipeline.py`
**Chemin** : `\\serveur_partage\BNP_Compliance\src\`
**Exécution** : `python pipeline.py`

**ENTRÉES (automatiquement déposées par le système bancaire) :**
- `transactions_jour.csv` → Transactions du jour
- `clients_referentiel.csv` → Base clients mise à jour

**SORTIES (à récupérer par Blue Prism) :**
- `alertes_compliance.csv` → Transactions suspectes
- `rapport_execution.json` → Métriques de traitement

**CODES DE RETOUR :**
- 0 : Succès, fichier généré
- 1 : Erreur données d'entrée
- 2 : Erreur traitement
- 3 : Fichier output non généré

**EXEMPLE DE COMMANDE DE TEST :**
```cmd
cd \\serveur_partage\BNP_Compliance\src
python pipeline.py --input-dir ..\input --output-dir ..\output