import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configuration pour la reproductibilité
np.random.seed(42)
random.seed(42)

print("🚀 GÉNÉRATION DES DONNÉES POUR PROJET BNP - RPA/IA\n")

# ============================================================================
# PARTIE 1 : GÉNÉRATION DES CLIENTS (30 clients)
# ============================================================================

print("📋 Génération de 30 clients...")

# Données de base
prenoms = ["Jean", "Marie", "Pierre", "Sophie", "Thomas", "Julie", "Nicolas", "Isabelle", "Alexandre", "Camille"]
noms = ["Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petit", "Durand", "Leroy", "Moreau"]
segments = ["Comptant", "Privilege", "Entreprise", "Institutionnel", "Digital"]
pays_europe = ["FR", "DE", "IT", "ES", "BE", "NL", "LU", "CH", "GB", "PT", "SE", "DK"]
industries = ["Technologie", "Finance", "Commerce", "Industrie", "Services", "Santé", "Immobilier", "Transport"]

clients_data = []
client_id_counter = 1

# Créer 5 clients de base avec des profils spécifiques (pour les scénarios de test)
base_clients = [
    ["CLT-001", "DUPONT Martin", "FR", "Moyen", "2020-03-15", "Comptant", 125000, "Particulier", "Non", 2],
    ["CLT-002", "SCHULZ GmbH", "DE", "Élevé", "2021-11-22", "Entreprise", 2500000, "Finance", "Oui", 3],
    ["CLT-003", "ROSSI SPA", "IT", "Faible", "2019-06-10", "Entreprise", 500000, "Industrie", "Non", 1],
    ["CLT-004", "JOHANSSON AB", "SE", "Moyen", "2022-05-30", "Entreprise", 750000, "Technologie", "Non", 2],
    ["CLT-005", "COSTA SILVA", "PT", "Élevé", "2023-01-14", "Comptant", 30000, "Particulier", "Non", 3]
]

for client in base_clients:
    clients_data.append(client)

# Générer 25 clients supplémentaires
for _ in range(25):
    client_id = f"CLT-{client_id_counter+5:03d}"
    client_id_counter += 1
    
    nom_complet = f"{random.choice(prenoms)} {random.choice(noms)}"
    
    # 30% de chances d'être une entreprise
    if random.random() < 0.3:
        nom_complet = f"{nom_complet} {random.choice(['SARL', 'SA', 'GmbH', 'Ltd', 'SPA'])}"
        segment = "Entreprise"
    else:
        segment = random.choices(segments, weights=[40, 20, 0, 5, 35])[0]
    
    pays = random.choice(pays_europe)
    
    # Niveau de risque basé sur des règles métier
    if pays in ["LU", "CH"]:
        risque = random.choices(["Faible", "Moyen", "Élevé"], weights=[50, 40, 10])[0]
    elif segment == "Entreprise":
        risque = random.choices(["Faible", "Moyen", "Élevé"], weights=[30, 50, 20])[0]
    elif segment == "Digital":
        risque = random.choices(["Faible", "Moyen", "Élevé"], weights=[40, 40, 20])[0]
    else:
        risque = random.choices(["Faible", "Moyen", "Élevé"], weights=[60, 30, 10])[0]
    
    # Date d'inscription
    jours_inscription = random.randint(0, 1825)
    date_inscription = (datetime.now() - timedelta(days=jours_inscription)).strftime("%Y-%m-%d")
    
    # Encours annuel
    if segment == "Entreprise":
        encours = round(random.uniform(50000, 5000000), 2)
    elif segment == "Institutionnel":
        encours = round(random.uniform(1000000, 10000000), 2)
    elif segment == "Privilege":
        encours = round(random.uniform(100000, 1000000), 2)
    else:
        encours = round(random.uniform(1000, 100000), 2)
    
    # Industrie et PEP
    if segment == "Entreprise":
        industrie = random.choice(industries)
        if industrie in ["Finance", "Immobilier"] and risque == "Faible":
            risque = "Moyen"
    else:
        industrie = "Particulier"
    
    est_pep = "Non"
    if random.random() < 0.05:
        est_pep = "Oui"
        risque = "Élevé"
    
    score_risque_map = {"Faible": 1, "Moyen": 2, "Élevé": 3}
    score_risque = score_risque_map[risque]
    
    clients_data.append([
        client_id, nom_complet, pays, risque, date_inscription,
        segment, round(encours, 2), industrie, est_pep, score_risque
    ])

# Créer DataFrame clients
df_clients = pd.DataFrame(clients_data, columns=[
    "Client_ID", "Nom", "Pays", "Niveau_Risque", "Date_Inscription",
    "Segment", "Encours_Annuel", "Industrie", "Est_PEP", "Score_Risque"
])

# Sauvegarde clients
df_clients.to_csv("clients.csv", index=False, sep=";", encoding="utf-8")
df_clients.to_excel("clients.xlsx", index=False)

print(f"✅ {len(df_clients)} clients générés avec succès!")
print(f"   - Risque Élevé: {sum(df_clients['Niveau_Risque'] == 'Élevé')}")
print(f"   - Risque Moyen: {sum(df_clients['Niveau_Risque'] == 'Moyen')}")
print(f"   - Risque Faible: {sum(df_clients['Niveau_Risque'] == 'Faible')}")
print(f"   - Clients PEP: {sum(df_clients['Est_PEP'] == 'Oui')}")

# ============================================================================
# PARTIE 2 : GÉNÉRATION DES TRANSACTIONS (60 transactions)
# ============================================================================

print("\n💸 Génération de 60 transactions...")

# Récupérer les IDs clients pour référence
client_ids = df_clients["Client_ID"].tolist()
client_risks = dict(zip(df_clients["Client_ID"], df_clients["Niveau_Risque"]))

# Paramètres
n_transactions = 60
devises = ["EUR", "USD", "GBP", "CHF"]
types_operation = ["Virement", "Retrait", "Paiement", "Dépôt", "Conversion", "Prélèvement"]
pays_risque = ["RU", "SY", "IR", "KP", "CU", "VE"]  # Pays sous sanctions

transactions_data = []

# Créer quelques contreparties suspectes pour les scénarios
contreparties_suspectes = {
    "US123456789": "OFAC Sanctions List",
    "RU987654321": "Liste noire UE - Sanctions Russie",
    "SY112233445": "OFAC SDN List",
    "XY9988776655": "Liste interne - Fraude confirmée",
    "IR5566778899": "Programme nucléaire iranien"
}

# Dates de début
start_date = datetime(2024, 1, 1)

for i in range(1, n_transactions + 1):
    transaction_id = f"TXN-{10000 + i}"
    
    # Client aléatoire avec biais vers les clients à risque
    client_id = random.choice(client_ids)
    if random.random() < 0.3:  # 30% de chance de prendre un client à risque
        clients_eleves = [cid for cid in client_ids if client_risks[cid] == "Élevé"]
        if clients_eleves:
            client_id = random.choice(clients_eleves)
    
    # Date avec regroupements suspects possibles
    if random.random() < 0.1:  # 10% de transactions regroupées (structuring suspect)
        date = start_date + timedelta(days=random.choice([10, 11, 12, 15, 16]))
    else:
        date = start_date + timedelta(days=random.randint(0, 30))
    
    # Montant avec différents schémas
    is_suspect = random.random() < 0.2  # 20% de transactions suspectes
    
    if is_suspect:
        # Schéma 1: Structuring (juste en dessous du seuil de 10k€)
        if random.random() < 0.5:
            montant = round(random.uniform(8000, 9999), 2)
            pattern = "STRUCTURING"
        # Schéma 2: Transaction très élevée
        else:
            montant = round(random.uniform(50000, 250000), 2)
            pattern = "GROS_MONTANT"
    else:
        montant = round(random.uniform(100, 50000), 2)
        pattern = "NORMAL"
    
    # Type d'opération
    if montant > 20000:
        type_op = "Virement"
    elif montant < 1000:
        type_op = random.choice(["Paiement", "Retrait", "Prélèvement"])
    else:
        type_op = random.choices(types_operation, weights=[40, 15, 20, 10, 5, 10])[0]
    
    # Bénéficiaire et pays
    if is_suspect and random.random() < 0.4:
        # Choisir une contrepartie suspecte
        beneficiaire, raison = random.choice(list(contreparties_suspectes.items()))
        pays_benef = beneficiaire[:2] if len(beneficiaire) >= 2 else "XX"
        commentaire = f"Contrepartie à risque: {raison}"
    else:
        # Bénéficiaire normal
        pays_benef = random.choice(["FR", "DE", "IT", "ES", "BE", "NL", "LU", "CH"])
        code_bank = random.randint(1000, 9999)
        code_guichet = random.randint(1000, 9999)
        num_compte = random.randint(10000000000, 99999999999)
        beneficiaire = f"{pays_benef}{code_bank}{code_guichet}{num_compte}"
        commentaire = "Transaction standard"
    
    # Statut basé sur les règles métier
    statut = "À traiter"
    priorite = "Normale"
    
    if pays_benef in pays_risque:
        statut = "ALERTE: Pays sous sanctions"
        priorite = "Haute"
    elif montant > 10000:
        statut = "Vérification seuil réglementaire"
        priorite = "Moyenne"
    elif client_risks[client_id] == "Élevé":
        statut = "Surveillance client risque élevé"
        priorite = "Moyenne"
    elif pattern == "STRUCTURING":
        statut = "Suspicion de structuring"
        priorite = "Haute"
    elif "OFAC" in commentaire or "Liste noire" in commentaire:
        statut = "ALERTE: Contrepartie sanctionnée"
        priorite = "Critique"
    
    # Devise
    if pays_benef == "US" or random.random() < 0.1:
        devise = "USD"
    elif pays_benef == "GB":
        devise = "GBP"
    elif pays_benef == "CH":
        devise = "CHF"
    else:
        devise = random.choices(devises, weights=[80, 10, 5, 5])[0]
    
    # Canal de transaction
    canal = random.choices(["Agence", "Internet", "Mobile", "Téléphone"], weights=[30, 40, 25, 5])[0]
    
    # Heure de la transaction
    heure = f"{random.randint(8, 20):02d}:{random.randint(0, 59):02d}"
    
    transactions_data.append([
        transaction_id, date.strftime('%Y-%m-%d'), heure, client_id, type_op,
        round(montant, 2), devise, beneficiaire, pays_benef, canal,
        statut, priorite, pattern, commentaire
    ])

# Créer DataFrame transactions
df_transactions = pd.DataFrame(transactions_data, columns=[
    "Transaction_ID", "Date", "Heure", "Client_ID", "Type_Operation",
    "Montant", "Devise", "Bénéficiaire", "Pays_Bénéficiaire", "Canal",
    "Statut_Compliance", "Priorité", "Pattern", "Commentaire"
])

# Sauvegarde transactions
df_transactions.to_csv("transactions.csv", index=False, sep=";", encoding="utf-8")
df_transactions.to_excel("transactions.xlsx", index=False)

print(f"✅ {len(df_transactions)} transactions générées avec succès!")
print(f"   - Alertes critiques: {sum(df_transactions['Priorité'] == 'Critique')}")
print(f"   - Transactions > 10k€: {sum(df_transactions['Montant'] > 10000)}")
print(f"   - Suspicion de structuring: {sum(df_transactions['Pattern'] == 'STRUCTURING')}")
print(f"   - Pays à risque: {sum(df_transactions['Pays_Bénéficiaire'].isin(pays_risque))}")

# ============================================================================
# PARTIE 3 : CRÉATION D'UN FICHIER DE CONFIGURATION
# ============================================================================

print("\n⚙️  Création du fichier de configuration...")

config_data = {
    "Paramètre": [
        "Seuil réglementaire",
        "Pays sous sanctions",
        "Seuil structuring",
        "Clients PEP à surveiller",
        "Montant vérification automatique",
        "Devises principales"
    ],
    "Valeur": [
        "10 000 EUR",
        ", ".join(pays_risque),
        "9 500 EUR (pour détection structuring)",
        str(sum(df_clients["Est_PEP"] == "Oui")),
        "100 000 EUR",
        "EUR, USD, GBP, CHF"
    ],
    "Description": [
        "Seuil de déclaration obligatoire (réglementation)",
        "Liste des pays sous sanctions internationales",
        "Seuil pour détection de structuring (montants fractionnés)",
        "Nombre de Personnes Politiquement Exposées dans la base",
        "Montant déclenchant une vérification renforcée",
        "Devises acceptées dans le système"
    ]
}

df_config = pd.DataFrame(config_data)
df_config.to_csv("config_règles_métier.csv", index=False, sep=";", encoding="utf-8")
df_config.to_excel("config_règles_métier.xlsx", index=False)

print("✅ Fichier de configuration créé!")

# ============================================================================
# RÉCAPITULATIF FINAL
# ============================================================================

print("\n" + "="*60)
print("📊 RÉCAPITULATIF DU PROJET GÉNÉRÉ")
print("="*60)

print(f"📁 Fichiers créés dans le dossier 'fichiers_exemple':")
print(f"   1. clients.csv / clients.xlsx → {len(df_clients)} clients")
print(f"   2. transactions.csv / transactions.xlsx → {len(df_transactions)} transactions")
print(f"   3. config_règles_métier.csv / .xlsx → Règles de compliance")

print(f"\n🔍 Métriques pour l'entretien BNP:")
print(f"   • {sum(df_clients['Niveau_Risque'] == 'Élevé')} clients à risque élevé")
print(f"   • {sum(df_clients['Est_PEP'] == 'Oui')} Personnes Politiquement Exposées (PEP)")
print(f"   • {sum(df_transactions['Montant'] > 10000)} transactions > 10k€ (seuil réglementaire)")
print(f"   • {sum(df_transactions['Priorité'] == 'Critique')} alertes critiques à traiter")
print(f"   • {sum(df_transactions['Pattern'] == 'STRUCTURING')} suspicions de structuring")

print(f"\n💡 Scénarios disponibles pour ta démo:")
print(f"   1. Détection de structuring (montants < 10k€ mais suspects)")
print(f"   2. Transactions vers pays sous sanctions")
print(f"   3. Clients PEP avec activité surveillée")
print(f"   4. Contreparties sur listes noires (OFAC)")

print(f"\n🎯 Conseil pour l'entretien:")
print(f"   'Ces données simulées incluent des schémas réels de surveillance")
print(f"   réglementaire que Blue Prism pourrait automatiser avec des règles métier")
print(f"   spécifiques et une brique IA pour la détection d'anomalies.'")

print("\n" + "="*60)
print("✅ GÉNÉRATION TERMINÉE - PRÊT POUR LA SEMAINE 2 (ARCHITECTURE)")
print("="*60)