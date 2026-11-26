# Guide utilisateur — GameAgent AI v0.15.0

## 1. Prérequis et installation

Windows 10/11 est la plateforme cible du launcher natif. Python 3.12+, Git et uv sont nécessaires. Les modules de recherche et les interfaces Qt sont aussi testés sur Ubuntu en CI, sans garantie de prise en charge complète des applications Windows.

Depuis PowerShell :

```powershell
git clone https://github.com/legobelindu93/GameAgent-AI.git
cd GameAgent-AI
uv sync --extra modern-ui --extra native-ui --extra vision --extra ocr
uv run python -m gameagent
```

Pour mettre à jour : sauvegarder les données locales, exécuter `git pull origin main`, puis répéter la synchronisation avec les extras voulus. Conserver tous les extras nécessaires dans une même commande : uv peut retirer ceux qui ne sont plus demandés.

| Extra | Usage |
|---|---|
| modern-ui | PySide6 / huit panels Qt |
| native-ui | pywebview et pywin32 sous Windows |
| vision | OpenCV et NumPy |
| ocr | RapidOCR / ONNX Runtime |
| video | Transcription locale faster-whisper |
| cloud-study | SDK Gemini pour vidéo distante (installation et appel réel à vérifier) |
| navigation | A* / MiniGrid |
| learning | Gymnasium / Stable Baselines3 PPO |

Le GPU n'est pas requis pour les packs, la recherche lexicale ou l'interface. Les traitements locaux vidéo/LLM peuvent être coûteux en CPU, RAM et temps. Les services distants nécessitent des clés et peuvent être payants.

## 2. Parcours des huit panels

| Panel | Accès direct (préfixe uv run python -m) |
|---|---|
| Bibliothèque | gameagent |
| Console | gameagent.qt_console --game brown_dust_2 |
| Research Factory | gameagent.qt_research |
| Connaissances | gameagent.qt_knowledge |
| Expert F2P | gameagent.qt_expert |
| Laboratoire | gameagent.qt_lab |
| Sources | gameagent.qt_sources |
| Simulation | gameagent.qt_simulation |

Le sélecteur de jeu change le contexte des modules multi-jeux. Les deux panels experts sont dédiés à Brown Dust 2. Les résultats s'affichent à droite et peuvent être copiés. Les traitements longs sont exécutés hors du thread d'affichage ; la fermeture d'un workbench actif est refusée jusqu'à la fin du traitement.

### Bibliothèque et console

1. Choisir le jeu, puis « Ouvrir le panel complet du jeu ».
2. Onglet Installation : rechercher les versions, sélectionner un fichier, confirmer son téléchargement. Le fichier n'est pas exécuté automatiquement.
3. Vérifier la provenance, la licence et les instructions de l'auteur ; installer ou extraire l'application manuellement.
4. Onglet Application : sélectionner l'exécutable de l'application tierce, pas celui du jeu. Pour les sources Python, préparer l'environnement selon la documentation d'origine.
5. Ouvrir l'application avec confirmation. Pour une WebUI, configurer une URL HTTP sur localhost ou 127.0.0.1 avec port, puis ouvrir la WebUI.
6. Si nécessaire, sélectionner Interface native, puis Embarquer la fenêtre. Seules les fenêtres du PID lancé depuis cette console sont éligibles. Détacher avant de fermer si nécessaire. L'intégration est expérimentale.
7. Utiliser Diagnostic pour obtenir la révision, les fichiers et les prérequis locaux.

Aucun automatisme de jeu n'est déclenché par le launcher. Respecter les règles applicables aux projets tiers.

### Research Factory — 19 commandes

| Groupe | Opérations |
|---|---|
| Découvrir | Sources, Rechercher, Cycle de recherche, Couverture indicative, Recherche autonome ciblée, Vérifier annonces |
| Étudier | Étudier vidéo YouTube, Recherche IA web, Importer notes / sous-titres, Compiler via API, Ouvrir une source |
| Packs | Installer pack initial, Installer les six packs, Importer pack, Exporter les six packs, Valider un pack |
| Compte et analyse | Importer compte, Conseil hors ligne, Benchmark local |

Premier usage : installer les six packs, choisir Brown Dust 2, lancer Conseil hors ligne avec une question sur la progression. Les résultats peuvent être insuffisants ou obsolètes. Les packs initiaux ne constituent pas une base exhaustive et leurs références nécessitent une vérification indépendante.

Pour ajouter une connaissance, sélectionner un document autorisé, renseigner l'URL et la version du jeu, puis importer. Les documents destinés à une API font l'objet d'une confirmation séparée. Vérifier chaque fiche candidate avant approbation et installation. Un hash valide ne prouve pas l'authenticité des données.

### Connaissances

Saisir une question ou un personnage et éventuellement un patch. Guides recherche les extraits FTS5 ; Personnages / builds interroge le catalogue ; Interroger l'IA utilise Ollama, à installer séparément. Exemple de modèle local : `ollama pull qwen2.5:3b`. Sans Ollama, les deux recherches restent disponibles.

### Expert F2P et laboratoire

Renseigner manuellement la progression, le type d'équipe, le blocage, l'objectif, le temps disponible, les diamants, les tickets et les costumes. Le plan heuristique ne constitue pas un optimum démontré.

Dans le laboratoire : importer un catalogue normalisé, tester `games/brown_dust_2/example_team.json` (statistiques fictives), choisir une capture pour l'OCR, confirmer les ressources avant enregistrement, étudier un fichier vidéo autorisé ou consulter les annonces et logs MFABD2. Le catalogue initial contient 65 noms, sans statistiques complètes. Le flux RSS et les chemins de logs restent à valider.

### Sources et simulation

Dans Sources, choisir un profil puis Actualiser. Les dépôts doivent être présents et leurs fichiers extraits localement. Le filtre et l'aperçu ne lancent aucun code tiers. Les actions de configuration/lancement d'application sont distinctes et explicites.

Simulation utilise des combats synthétiques, trois stratégies, des démonstrations et une mémoire SQLite. La comparaison d'images utilise des fichiers locaux. Aucun état de jeu réel n'est modifié.

## 3. Services distants (facultatifs)

Définir seulement les variables nécessaires dans la session PowerShell. Ne pas publier les clés dans Git, les captures ou les logs.

| Variable | Fonction |
|---|---|
| YOUTUBE_API_KEY | Métadonnées publiques YouTube |
| BRAVE_SEARCH_API_KEY | Découverte web |
| OPENAI_API_KEY | Compilation de notes / recherche distante |
| GAMEAGENT_REMOTE_MODEL | Modèle de compilation |
| GAMEAGENT_WEB_MODEL | Modèle compatible Responses + web_search |
| GEMINI_API_KEY | Étude distante d'une vidéo |
| GAMEAGENT_VIDEO_MODEL | Modèle compatible vidéo YouTube |

Exemple de configuration (remplacer les valeurs) :

```powershell
$env:OPENAI_API_KEY = "VOTRE_CLE"
$env:GAMEAGENT_WEB_MODEL = "MODELE_COMPATIBLE"
```

Aucun service n'est nécessaire pour les packs initiaux. Les appels réels, la disponibilité des modèles, le SDK et les tarifs ne sont pas validés par les tests CI. Ne pas analyser de contenu sans droits.

## 4. Données et apparence

Exécuter depuis la racine du dépôt. Les configurations, bases, fichiers importés et résultats sont locaux sous data/ (voir la référence technique). Sauvegarder ce dossier avant réinstallation ; il peut contenir des informations de compte et des journaux. Ne pas le publier.

Pour personnaliser un jeu, placer une image autorisée dans assets/games/ID/banner.png (jpg/webp acceptés) et redémarrer. Les illustrations par défaut sont générées localement.

## 5. Dépannage

| Symptôme | Action |
|---|---|
| Ancienne UI au lancement | Installer modern-ui, vérifier uv run python -c "import PySide6" |
| Erreur de dépendance | Ajouter l'extra requis dans la commande uv sync |
| Application non configurée | Vérifier le chemin de l'exécutable ou la disponibilité des sources et de l'environnement |
| Port occupé | Fermer l'instance concernée, vérifier le port configuré |
| Fenêtre non détectée / mal dimensionnée | Utiliser le mode externe ou le launcher classique ; ne pas contourner les permissions |
| Sources vides | Vérifier data/upstream/ID et l'extraction des fichiers, puis Actualiser |
| Aucun résultat de recherche | Installer le pack, élargir la requête, vérifier le patch |
| Erreur API/Ollama | Vérifier service, modèle, droits, clé et quota ; utiliser les fonctions hors ligne |
| Erreur OCR | Vérifier l'extra ocr et sélectionner une capture lisible |

Secours : `uv run python -m gameagent --classic` ou `uv run python -m gameagent.launcher_ui --game brown_dust_2`.

Pour signaler un bug, préciser la version, l'OS, le panel, les étapes, le message exact et une capture expurgée des clés et données personnelles. Voir [validation](validation.md).
