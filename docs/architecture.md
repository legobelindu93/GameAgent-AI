# Architecture — v0.15.0

```mermaid
flowchart TD
    Entry["python -m gameagent"] --> UI["Obsidian Studio / Qt Widgets"]
    Entry --> Classic["Tkinter / secours"]
    UI --> Console["Console des jeux"]
    UI --> Research["Research Factory / Knowledge / Expert / Lab"]
    UI --> Sources["Explorateur de sources"]
    UI --> Sim["Simulation synthétique"]
    Console --> Bridge["bridges / native / installations / dependencies"]
    Bridge --> Third["Applications tierces indépendantes"]
    Console --> Host["Qt native surface / Win32 host"]
    Research --> Packs["packs / factory / research_engine"]
    Research --> BD["bd2_expert / bd2_tactics / OCR"]
    Packs --> Index["SQLite FTS5 par jeu"]
    Research --> Catalog["Catalogue SQLite"]
    Packs --> Remote["APIs facultatives / consentement"]
    Research --> Local["Ollama facultatif"]
    Sources --> LocalRepo["Sources locales / lecture seule"]
    Sim --> Engine["engine / planner / imitation / memory"]
```

La bibliothèque lance les workbenches dans des processus Python distincts. Les workbenches partagent leurs composants visuels mais conservent leurs propres états et traitements. Les modules métier restent indépendants de Qt. Les configurations de profil sont isolées ; le code amont n'est pas intégré au moteur de décision.

L'hébergement Win32 est un adaptateur de fenêtre, pas une API de tâches. Les modules IA n'envoient pas de commandes au client réel. La recherche distante produit des candidats, soumis à vérification et import explicites. Le simulateur est une expérience synthétique indépendante.

Voir [référence technique](technical-reference.md) pour les contrats et limites.
