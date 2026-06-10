# 🇸🇳 ORL au Sénégal - Plateforme d'Intelligence Artificielle

**Plateforme complète de gestion et d'analyse des données ORL au Sénégal** incluant universités, structures hospitalières, praticiens et étudiants en DES.

## 📊 Vue d'ensemble

- **12 universités** ORL (7 publiques + 5 privées)
- **56 structures** hospitalières et cliniques
- **108 praticiens** ORL
- **185 étudiants** en DES (65 DES1, 56 DES2, 48 DES3, 16 DES4)
- **Dashboard interactif** Streamlit
- **API RESTful** FastAPI

## 🎯 Caractéristiques

✅ Base de données Oracle complète
✅ Dashboard 5 onglets (Streamlit)
✅ API 10+ endpoints
✅ Visualisations Plotly avancées
✅ Docker Compose automatisé
✅ Production-ready

## 🚀 Démarrage rapide

### Prérequis
- Docker & Docker Compose
- Git

### Installation

```bash
git clone https://github.com/diallobaykarim-glitch/ORLSenegalBkd10juin2026.git
cd ORLSenegalBkd10juin2026

docker-compose up -d --build
```

### Accès

- **Dashboard** : http://localhost:8502
- **API Docs** : http://localhost:8001/docs
- **Oracle** : localhost:1523 (sys/oracle)

## 📈 Données

### Universités (12)

**Publiques (7)** :
- UCAD-Dakar ✓ DES
- UIB-Thiès ✓ DES
- UAS-Ziguinchor ✓ DES
- UGB-Saint-Louis
- UAD-Bambey
- UADB-Kaolack
- UASZ-Kolda

**Privées (5)** :
- EINS, EU, IPFORMED, USSD, HmpthB (Dakar)

### Structures (56)

**Publiques (43)** :
- 18 à Dakar (HEAR, HOGIP, Fann, etc.)
- 25 en Régions

**Privées (13)** :
- 11 à Dakar
- 2 en Régions

### Ressources Humaines

- **108 praticiens ORL**
- **185 étudiants en DES** :
  - 65 DES1
  - 56 DES2
  - 48 DES3
  - 16 DES4

## 🔌 API Endpoints

```
GET /                              # Home
GET /health                        # Health check
GET /statistics/summary            # Résumé global
GET /statistics/universities       # Stats universités
GET /statistics/structures         # Stats structures
GET /statistics/practitioners      # Stats praticiens
GET /statistics/students           # Stats étudiants
GET /universities                  # Toutes les universités
GET /structures                    # Toutes les structures
```

## 📊 Dashboard

### Onglet 1 : Vue Générale
- Métriques KPI
- Distribution globale (pie chart)

### Onglet 2 : Universités
- Public vs Privé
- Avec/Sans DES
- Liste complète

### Onglet 3 : Structures
- Par secteur (bar chart)
- Par région (bar chart)
- Liste complète

### Onglet 4 : Praticiens
- Distribution secteur/région
- Expérience moyenne
- Détails

### Onglet 5 : Étudiants
- Distribution par année DES
- Distribution par région
- Statistiques détaillées

## 📁 Structure

```
.
├── docker-compose.yml         # Docker config
├── .env                       # Variables env
├── .gitignore                 # Git ignore
├── generate_senegal_orl_data.py  # Générateur dataset
├── api/
│   ├── Dockerfile
│   ├── main.py               # Endpoints FastAPI
│   └── requirements.txt
└── dashboard/
    ├── Dockerfile
    ├── app.py                # Dashboard Streamlit
    └── requirements.txt
```

## 🐳 Commandes Docker

```bash
# Démarrer
docker-compose up -d

# Arrêter
docker-compose down

# Logs
docker-compose logs -f api

# Rebuild
docker-compose up -d --build
```

## 🔧 Génération données

Après le démarrage :

```bash
python generate_senegal_orl_data.py
```

## 📚 Données complètes

**Universités publiques avec DES ORL** :
1. UCAD-Dakar
2. UIB-Thiès
3. UAS-Ziguinchor

**Structures publiques à Dakar** (18) :
HEAR, HOGIP, Fann, HPD, HMO, IHS, DllJm, SmMncpal, Pkn, GsprdCmr, RBdn, Wkm, KrMssr, aBssNDw, PMSghr, CMIA, Rfsqe, HED

**Structures privées à Dakar** (11) :
ClnqCp, ClnqMdln, Ath, NAT, YnssLrq, NdmYctm, EMD, NdngPlr, MDng, Mygu, Aldo

**Régions** :
Dakar, Thiès, Saint-Louis, Ziguinchor, Kaolack, Kolda, Bambey

## 🎯 Fonctionnalités futures

- [ ] Export PDF rapports
- [ ] Authentification utilisateur
- [ ] Carte interactive régions
- [ ] Analyse tendances
- [ ] Tests automatisés

## 🔐 Sécurité

⚠️ **Développement seulement**
- Mot de passe Oracle en clair
- Sans authentification

**Production** :
- Docker Secrets
- JWT authentication
- SSL/TLS

## 👨‍💻 Auteur

**Diallo Baykarim**
- GitHub: https://github.com/diallobaykarim-glitch

## 📜 License

Projet éducatif - Usage libre

---

**Dernière mise à jour** : 10 Juin 2026
**Status** : 🚀 Production Ready
