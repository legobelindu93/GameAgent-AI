"""Visual identity and informational feature categories for each game."""
from pathlib import Path
from .profiles import ROOT

GAMES={
"nikke":("#dc506a","NK","Action / Shooter",["Missions quotidiennes","Avant-poste","Simulation Room","Gestion des récompenses"]),
"brown_dust_2":("#c69a64","BD","RPG tactique",["Routines quotidiennes","Activités","Configuration du compte","Gestion des ressources"]),
"genshin_impact":("#53b9b0","GI","Action RPG / Monde ouvert",["Navigation","Collecte","Combat","Donjons"]),
"wuthering_waves":("#7a9de0","WW","Action RPG / Monde ouvert",["Activités","Équipes","Combat","Reconnaissance visuelle"]),
"neverness_to_everness":("#e5ad49","NE","Action RPG / Monde urbain",["Exploration","Activités","Configuration","Reconnaissance visuelle"]),
"honkai_star_rail":("#b093ed","HS","RPG au tour par tour",["Missions quotidiennes","Énergie","Expéditions","Activités"]),
}
ASSETS=ROOT.parent/"assets"/"games"

def identity(game):
    accent,initials,genre,features=GAMES[game]
    return {"accent":accent,"initials":initials,"genre":genre,"features":features}

def artwork(game,kind):
    if game not in GAMES or kind not in ("banner","logo"):raise ValueError("Invalid artwork")
    for ext in ("png","jpg","jpeg","webp"):
        path=ASSETS/game/(kind+"."+ext)
        if path.is_file():return path
    return None
